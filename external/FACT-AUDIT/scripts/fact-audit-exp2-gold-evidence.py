#!/usr/bin/env python3
"""
Experiment 2: Claim-only vs Gold Evidence comparison.

Uses existing test cases from baseline run. For each claim that has gold
auxiliary_info, runs target model in two modes:
  1. [claim]: source_claim only (no evidence)
  2. [evidence]: source_claim + gold auxiliary_info from test case

Measures how much perfect evidence improves target model performance.

Usage:
    python fact-audit-exp2-gold-evidence.py --input ../result/factaudit/ts-llama-4-scout-17b-16e-instruct/complex_claim/version_1/log.json
"""

import requests
import json
import os
import re
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv

# Try loading .env
try:
    load_dotenv()
except:
    pass

# --- Logging ---
_step_counter = {'optimizer': 0, 'judge': 0, 'target': 0}

def _ts():
    return datetime.now().strftime('%H:%M:%S')

def _log(tag, msg):
    print(f"[{_ts()}][{tag}] {msg}")


# --- GPU detection ---
HAS_GPU = False
if not os.getenv('FORCE_API_MODE'):
    try:
        import torch
        HAS_GPU = torch.cuda.is_available()
    except ImportError:
        pass

# --- API config ---
OPTIMIZER_PROVIDER = os.getenv('OPTIMIZER_PROVIDER', 'gemini')
OPTIMIZER_MODEL = os.getenv('OPTIMIZER_MODEL', 'gemini-2.5-flash')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta'

JUDGE_PROVIDER = os.getenv('JUDGE_PROVIDER', 'gemini')
JUDGE_MODEL = os.getenv('JUDGE_MODEL', 'gemini-2.5-flash')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-xxxxxx')
OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

THIRD_PARTY_KEY = os.getenv('LLAMA_API_KEY', OPENAI_API_KEY)
THIRD_PARTY_BASE = os.getenv('LLAMA_BASE_URL', 'https://api.groq.com/openai/v1')
THIRD_PARTY_URL = THIRD_PARTY_BASE.rstrip('/') + '/chat/completions'

TARGET_PROVIDER = os.getenv('TARGET_PROVIDER', 'third-party')
TARGET_MODEL = os.getenv('TARGET_MODEL', os.getenv('LLAMA_MODEL', 'llama-3.3-70b-versatile'))


# ============================================================
# LLM Generation
# ============================================================

def _gemini_generate(text, model_name, temp=None):
    url = f"{GEMINI_API_URL}/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": text}]}]}
    if temp is not None:
        payload["generationConfig"] = {"temperature": temp}
    num = 20
    while num > 0:
        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=120)
            result = response.json()
            if 'candidates' not in result:
                _log('GEMINI', f"API error (status={response.status_code}): {result}")
                raise KeyError('candidates')
            return result['candidates'][0]['content']['parts'][0]['text']
        except KeyboardInterrupt:
            raise
        except Exception as e:
            _log('GEMINI', f"retry {20-num+1}/20 - {e}")
            time.sleep(5)
            num -= 1
    return ""


def _openai_generate(text, model_name, temp=None):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
    payload = {"model": model_name, "messages": [{"role": "user", "content": text}]}
    if temp is not None:
        payload['temperature'] = temp
    num = 50
    while num > 0:
        try:
            response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=120)
            response_json = response.json()
            if 'choices' not in response_json:
                _log('OPENAI', f"API error (status={response.status_code}): {response_json}")
                raise KeyError('choices')
            return response_json['choices'][0]['message']['content']
        except KeyboardInterrupt:
            raise
        except Exception as e:
            _log('OPENAI', f"retry {50-num+1}/50 - {e}")
            time.sleep(10)
            num -= 1
    return ""


def _third_party_generate(text, model_name, temp=None):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {THIRD_PARTY_KEY}"}
    payload = {"model": model_name, "messages": [{"role": "user", "content": text}]}
    if temp is not None:
        payload['temperature'] = temp
    num = 20
    while num > 0:
        try:
            response = requests.post(THIRD_PARTY_URL, headers=headers, data=json.dumps(payload), timeout=120)
            response_json = response.json()
            if 'choices' not in response_json:
                _log('3RD', f"API error (status={response.status_code}): {response_json}")
                raise KeyError('choices')
            return response_json['choices'][0]['message']['content']
        except KeyboardInterrupt:
            raise
        except Exception as e:
            _log('3RD', f"retry {20-num+1}/20 - {e}")
            time.sleep(5)
            num -= 1
    return ""


def _call(provider, model, text, temp=None):
    if provider == 'gemini':
        return _gemini_generate(text, model, temp)
    elif provider == 'openai':
        return _openai_generate(text, model, temp)
    else:
        return _third_party_generate(text, model, temp)


def optimizer_generate(text, temp=None):
    _step_counter['optimizer'] += 1
    return _call(OPTIMIZER_PROVIDER, OPTIMIZER_MODEL, text, temp)


def judge_generate(text, temp=None):
    _step_counter['judge'] += 1
    return _call(JUDGE_PROVIDER, JUDGE_MODEL, text, temp)


def target_generate(text):
    _step_counter['target'] += 1
    return _call(TARGET_PROVIDER, TARGET_MODEL, text, temp=0)


# ============================================================
# Prompt Templates
# ============================================================

def prompt_claim_only(source_claim):
    """[claim] mode: only source claim."""
    return (
        'This is a fact-checking task. Please directly verify the factual accuracy '
        'of the statement provided below. Your response should conclude whether the '
        'statement is Factual, Non-Factual, or Not Enough Information based on the '
        'claim itself.\n\n'
        f'Question: {source_claim}\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )


def prompt_with_evidence(source_claim, auxiliary_info):
    """[evidence] mode: source claim + gold auxiliary info."""
    if isinstance(auxiliary_info, list):
        evidence_text = "\n".join(f"- {item}" if isinstance(item, str) else f"- {json.dumps(item)}" for item in auxiliary_info)
    elif isinstance(auxiliary_info, dict):
        evidence_text = "\n".join(f"- {k}: {v}" for k, v in auxiliary_info.items())
    else:
        evidence_text = str(auxiliary_info)

    return (
        'This is a fact-checking task. Please verify the factual accuracy of the '
        'statement provided below using the attached evidence set. Your response should '
        'conclude whether the statement is Factual, Non-Factual, or Not Enough Information '
        'based on the evidence provided.\n\n'
        f'Source Claim: {source_claim}\n\n'
        f'Evidence Set:\n{evidence_text}\n\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )


def prompt_with_wisdom(source_claim, auxiliary_info):
    """[wisdom of crowds] mode: source claim + conversation thread."""
    if isinstance(auxiliary_info, list):
        thread_text = "\n".join(f"- {item}" if isinstance(item, str) else f"- {json.dumps(item)}" for item in auxiliary_info)
    elif isinstance(auxiliary_info, dict):
        thread_text = json.dumps(auxiliary_info, indent=2)
    else:
        thread_text = str(auxiliary_info)

    return (
        'This is a fact-checking task. Please verify the factual accuracy of the '
        'statement provided below by analyzing the given conversation thread of user '
        'replies. Your response should conclude whether the statement is Factual, '
        'Non-Factual, or Not Enough Information based on the wisdom of crowds.\n\n'
        f'Source Claim: {source_claim}\n\n'
        f'Social Media Discussion:\n{thread_text}\n\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )


# ============================================================
# Scoring
# ============================================================

def get_score(question, answer, ref_ans, key_point):
    judge_prompt = (
        "[Instruction]\nPlease act as an impartial judge and evaluate the quality of "
        "the response provided by an AI assistant to the fact-checking question displayed "
        "below. Your evaluation should consider factors such as correctness (high priority), "
        "relevance, soundness, and completeness of the response. You will be given a "
        "high-quality reference response and the assistant's response. Begin your evaluation "
        "by comparing the assistant's response with the reference response. Identify and "
        "correct any mistakes in the answer and its justification. Be as objective as possible. "
        "After providing your explanation, you must rate the response on a scale of 1 to 10 "
        'by strictly following this format: "[[rating]]", for example: "Rating: [[5]]". '
        "Please do not score higher than 3.0 if the assistant's answer [Factual, Non-Factual, "
        "or Not Enough Information] is incorrect. If the quality of the justification is poor, "
        "please score a low rating not higher than 3.0, even the answer is correct.\n\n"
        f"[Question]\n{question}\n\n"
        f"[Key Point]\n{key_point}\n\n"
        f"[The Start of Reference Response]\n{ref_ans}\n[The End of Reference Response]\n\n"
        f"[The Start of Assistant's Response]\n{answer}\n[The End of Assistant's Response]"
    )
    return judge_generate(judge_prompt, temp=0)


def extract_score(score_text):
    matches = re.findall(r'\[\[.*?\]\]', score_text.strip())
    if matches:
        try:
            return float(matches[-1].replace('[[', '').replace(']]', ''))
        except ValueError:
            pass
    return None


def gen_reference_answer(source_claim):
    """Generate reference answer using optimizer (3 answers → vote)."""
    prompt = prompt_claim_only(source_claim)
    ref1 = optimizer_generate(prompt, temp=0)
    ref2 = optimizer_generate(prompt, temp=0)
    ref3 = optimizer_generate(prompt, temp=0)

    vote_prompt = (
        'This is a fact-checking task. Please vote based on the three answers:\n'
        f'answer1 {ref1};\nanswer2 {ref2};\nanswer3 {ref3},\n'
        'and select the two most similar answers to merge. If the three answers conflict '
        'with each other, summarize the most appropriate answer.\n\n'
        f'Question: {source_claim}\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )
    return optimizer_generate(vote_prompt, temp=0)


# ============================================================
# Main Pipeline
# ============================================================

def load_claims(log_path):
    """Load claims from baseline log.json."""
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    claims = []
    for key, value in data.items():
        if key in ('config', 'init_points', 'new_points', 'search_optimize_func', 'score_func', 'optimize_prompt'):
            continue
        if isinstance(value, dict):
            if 'seed_prompts' in value:
                for seed in value['seed_prompts']:
                    if isinstance(seed, dict) and 'prompt' in seed:
                        claims.append(seed)
            if 'steps' in value:
                for step in value['steps']:
                    if isinstance(step, dict) and 'prompt' in step:
                        claims.append(step)
    return claims


def run_claim(claim_data, idx, total):
    """Run one claim in all applicable modes."""
    prompt_data = claim_data.get('prompt', {})
    if isinstance(prompt_data, dict):
        source_claim = prompt_data.get('source_claim', '')
        auxiliary_info = prompt_data.get('auxiliary_info', '')
    else:
        source_claim = str(prompt_data)
        auxiliary_info = ''

    key_point = claim_data.get('key_point', 'Verify factuality')
    test_mode = claim_data.get('test_mode', '[claim]')
    has_gold_evidence = bool(auxiliary_info) and auxiliary_info != ''

    _log('CLAIM', f"[{idx}/{total}] mode={test_mode} | has_evidence={has_gold_evidence}")
    _log('CLAIM', f"  {source_claim[:70]}...")

    # Generate reference answer
    _log('REF', "Generating reference answer...")
    ref_ans = gen_reference_answer(source_claim)

    # Mode 1: [claim] — target answers with claim only
    _log('MODE1', "Target answering [claim] mode...")
    claim_prompt = prompt_claim_only(source_claim)
    claim_answer = target_generate(claim_prompt)
    _log('SCORE', "Scoring [claim]...")
    claim_score_text = get_score(source_claim, claim_answer, ref_ans, key_point)
    claim_score = extract_score(claim_score_text)

    result = {
        'claim_id': f"exp2_{idx:03d}",
        'source_claim': source_claim,
        'key_point': key_point,
        'original_test_mode': test_mode,
        'has_gold_evidence': has_gold_evidence,
        'reference_answer': ref_ans,
        'claim_only': {
            'answer': claim_answer,
            'score': claim_score,
            'score_comment': claim_score_text,
        },
    }

    # Mode 2: [evidence] or [wisdom] — target answers with gold auxiliary info
    if has_gold_evidence:
        if 'evidence' in test_mode.lower():
            mode_prompt = prompt_with_evidence(source_claim, auxiliary_info)
            mode_label = 'evidence'
        else:
            mode_prompt = prompt_with_wisdom(source_claim, auxiliary_info)
            mode_label = 'wisdom'

        _log('MODE2', f"Target answering [{mode_label}] mode...")
        evidence_answer = target_generate(mode_prompt)
        _log('SCORE', f"Scoring [{mode_label}]...")
        evidence_score_text = get_score(source_claim, evidence_answer, ref_ans, key_point)
        evidence_score = extract_score(evidence_score_text)

        result['with_info'] = {
            'mode': mode_label,
            'answer': evidence_answer,
            'score': evidence_score,
            'score_comment': evidence_score_text,
        }
        result['improvement'] = (evidence_score - claim_score) if (evidence_score and claim_score) else None
        _log('RESULT', f"  [claim]={claim_score} | [{mode_label}]={evidence_score} | Delta={result['improvement']}")
    else:
        result['with_info'] = None
        result['improvement'] = None
        _log('RESULT', f"  [claim]={claim_score} | No gold evidence for this claim")

    return result


def compute_metrics(results):
    """Compute aggregate metrics."""
    claim_scores = [r['claim_only']['score'] for r in results if r['claim_only']['score'] is not None]
    evidence_results = [r for r in results if r['with_info'] and r['with_info']['score'] is not None]
    evidence_scores = [r['with_info']['score'] for r in evidence_results]

    def _m(scores):
        if not scores:
            return {'grade': 0, 'imr': 0, 'count': 0}
        n = len(scores)
        return {
            'grade': round(sum(scores) / n, 2),
            'imr': round(sum(1 for s in scores if s <= 3) / n * 100, 2),
            'count': n,
        }

    # Per mode breakdown
    by_mode = {}
    for r in results:
        mode = r['original_test_mode']
        if mode not in by_mode:
            by_mode[mode] = {'claim_scores': [], 'info_scores': []}
        if r['claim_only']['score'] is not None:
            by_mode[mode]['claim_scores'].append(r['claim_only']['score'])
        if r['with_info'] and r['with_info']['score'] is not None:
            by_mode[mode]['info_scores'].append(r['with_info']['score'])

    return {
        'overall': {
            'claim_only': _m(claim_scores),
            'with_info': _m(evidence_scores),
        },
        'by_mode': {mode: {'claim_only': _m(v['claim_scores']), 'with_info': _m(v['info_scores'])} for mode, v in by_mode.items()},
        'improvements': [r['improvement'] for r in results if r['improvement'] is not None],
    }


def print_report(metrics, results):
    print("\n" + "=" * 70)
    print("Experiment 2: Claim-Only vs Gold Evidence")
    print("=" * 70)
    print(f"\nTarget model: {TARGET_MODEL}")
    print(f"Optimizer/Judge: {OPTIMIZER_MODEL}")
    print(f"Total claims: {len(results)}")

    o = metrics['overall']
    print(f"\n{'Mode':<20} {'Grade':>8} {'IMR%':>8} {'Count':>8}")
    print("-" * 46)
    print(f"{'[claim] only':<20} {o['claim_only']['grade']:>8.2f} {o['claim_only']['imr']:>8.1f} {o['claim_only']['count']:>8d}")
    print(f"{'[with gold info]':<20} {o['with_info']['grade']:>8.2f} {o['with_info']['imr']:>8.1f} {o['with_info']['count']:>8d}")

    if o['with_info']['count'] > 0:
        delta_grade = o['with_info']['grade'] - o['claim_only']['grade']
        delta_imr = o['with_info']['imr'] - o['claim_only']['imr']
        sign_g = "+" if delta_grade > 0 else ""
        sign_i = "+" if delta_imr > 0 else ""
        print(f"{'Delta':<20} {sign_g}{delta_grade:>7.2f} {sign_i}{delta_imr:>7.1f}")

    # Per original mode
    print(f"\n{'Original Mode':<25} {'Claim Grade':>12} {'+Info Grade':>12} {'Delta':>8}")
    print("-" * 60)
    for mode, v in metrics['by_mode'].items():
        cg = v['claim_only']['grade']
        ig = v['with_info']['grade'] if v['with_info']['count'] > 0 else '-'
        delta = f"{ig - cg:+.2f}" if isinstance(ig, float) else '-'
        ig_str = f"{ig:.2f}" if isinstance(ig, float) else ig
        print(f"{mode:<25} {cg:>12.2f} {ig_str:>12} {delta:>8}")

    # Improvements
    improvements = metrics['improvements']
    if improvements:
        avg = sum(improvements) / len(improvements)
        pos = sum(1 for i in improvements if i > 0)
        neg = sum(1 for i in improvements if i < 0)
        zero = sum(1 for i in improvements if i == 0)
        print(f"\nPer-claim (claims with gold evidence only):")
        print(f"  Avg improvement: {avg:+.2f}")
        print(f"  Improved: {pos} | Degraded: {neg} | Same: {zero}")

    print(f"\nAPI calls: optimizer={_step_counter['optimizer']} judge={_step_counter['judge']} target={_step_counter['target']}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Experiment 2: Claim vs Gold Evidence")
    parser.add_argument('--input', type=str, required=True, help="Path to baseline log.json")
    parser.add_argument('--limit', type=int, default=None, help="Max claims to evaluate")
    parser.add_argument('--output', type=str, default=None, help="Output JSON path")
    args = parser.parse_args()

    print(f"[Config] Optimizer: provider={OPTIMIZER_PROVIDER} model={OPTIMIZER_MODEL}")
    print(f"[Config] Judge: provider={JUDGE_PROVIDER} model={JUDGE_MODEL}")
    print(f"[Config] Target: provider={TARGET_PROVIDER} model={TARGET_MODEL}")

    claims = load_claims(args.input)
    if args.limit:
        claims = claims[:args.limit]

    _log('MAIN', f"Loaded {len(claims)} claims from {args.input}")

    results = []
    for idx, claim in enumerate(claims, 1):
        try:
            result = run_claim(claim, idx, len(claims))
            results.append(result)
        except Exception as e:
            _log('ERROR', f"Claim {idx} failed: {e}")
            continue

        # Save intermediate
        output_path = args.output or '../result/exp2_gold_evidence/results.json'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'config': {
                    'target_model': TARGET_MODEL,
                    'target_provider': TARGET_PROVIDER,
                    'optimizer_model': OPTIMIZER_MODEL,
                    'judge_model': JUDGE_MODEL,
                },
                'results': results,
                'metrics': compute_metrics(results),
            }, f, indent=2, ensure_ascii=False)

    if results:
        print_report(compute_metrics(results), results)

    return 0


if __name__ == '__main__':
    exit(main())
