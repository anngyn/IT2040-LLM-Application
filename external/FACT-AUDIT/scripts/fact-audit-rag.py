#!/usr/bin/env python3
"""
FACT-AUDIT + RAG: Wikipedia retrieval-augmented fact-checking evaluation.

This script extends the paper's fact-audit pipeline by adding real Wikipedia
retrieval. It runs claims in two modes:
  1. Baseline [claim]: LLaMA answers with source claim only (no evidence)
  2. RAG [evidence]: LLaMA answers with retrieved Wikipedia evidence

Then compares scores to measure RAG improvement.

Usage:
    python fact-audit-rag.py --category "Numerical Inaccuracies" --limit 10
    python fact-audit-rag.py --input ../result/factaudit/gpt-4o/numerical_inaccuracies/version_0/log.json
"""

import requests
import json
import os
import re
import argparse
import time
from datetime import datetime
from urllib.parse import urlencode
from urllib import request as urllib_request

# --- Logging ---
_step_counter = {'gpt4o': 0, 'gpt4o_mini': 0, 'llama': 0, 'wiki_search': 0, 'wiki_extract': 0}

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

if HAS_GPU:
    from transformers import AutoModelForCausalLM, AutoTokenizer

# --- API config (same as fact-audit.py) ---
# Optimizer
OPTIMIZER_PROVIDER = os.getenv('OPTIMIZER_PROVIDER', 'gemini')
OPTIMIZER_MODEL = os.getenv('OPTIMIZER_MODEL', 'gemini-2.5-flash')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta'

# Judge
JUDGE_PROVIDER = os.getenv('JUDGE_PROVIDER', 'gemini')
JUDGE_MODEL = os.getenv('JUDGE_MODEL', 'gemini-2.5-flash')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-xxxxxx')
OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')

# Third-party (target model)
THIRD_PARTY_KEY = os.getenv('LLAMA_API_KEY', OPENAI_API_KEY)
THIRD_PARTY_BASE = os.getenv('LLAMA_BASE_URL', 'https://api.groq.com/openai/v1')
THIRD_PARTY_URL = THIRD_PARTY_BASE.rstrip('/') + '/chat/completions'

# Target
TARGET_PROVIDER = os.getenv('TARGET_PROVIDER', 'third-party')
TARGET_MODEL = os.getenv('TARGET_MODEL', os.getenv('TARGET_MODEL', 'llama-3.3-70b-versatile'))

device = 'cuda:0' if HAS_GPU else 'cpu'

# --- Wikipedia Retriever Config ---
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_TOP_K = int(os.getenv('WIKI_TOP_K', '5'))
WIKI_MAX_CHARS = int(os.getenv('WIKI_MAX_CHARS', '1500'))
WIKI_DELAY = float(os.getenv('WIKI_DELAY', '1.0'))


# ============================================================
# LLM Generation Functions (same as fact-audit.py)
# ============================================================

def _gemini_generate(text, model_name, temp=None):
    """Call Gemini API directly."""
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
    """Call OpenAI API directly."""
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
    """Call third-party OpenAI-compatible API."""
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
    """Route call to correct provider."""
    if provider == 'gemini':
        return _gemini_generate(text, model, temp)
    elif provider == 'openai':
        return _openai_generate(text, model, temp)
    else:
        return _third_party_generate(text, model, temp)


def gpt4o_turbo_generate(text, temp=None):
    """Optimizer: generate ref answers."""
    _step_counter['gpt4o'] += 1
    return _call(OPTIMIZER_PROVIDER, OPTIMIZER_MODEL, text, temp)


def gpt4omini_turbo_generate(text, temp=None):
    """Judge: score target answers."""
    _step_counter['gpt4o_mini'] += 1
    return _call(JUDGE_PROVIDER, JUDGE_MODEL, text, temp)


def llama_generate(text):
    """Target model generate."""
    _step_counter['llama'] += 1
    return _call(TARGET_PROVIDER, TARGET_MODEL, text, temp=0)


print(f"[Config] Optimizer: provider={OPTIMIZER_PROVIDER} model={OPTIMIZER_MODEL}")
print(f"[Config] Judge: provider={JUDGE_PROVIDER} model={JUDGE_MODEL}")
print(f"[Config] Target: provider={TARGET_PROVIDER} model={TARGET_MODEL}")


# ============================================================
# Wikipedia Retriever
# ============================================================

def _wiki_search(query, limit=5, retries=3):
    """Search Wikipedia, return list of {title, snippet}."""
    _step_counter['wiki_search'] += 1
    params = urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    })
    url = f"{WIKI_API}?{params}"
    for attempt in range(retries):
        try:
            req = urllib_request.Request(url, headers={"User-Agent": "FACT-AUDIT-RAG/1.0"})
            with urllib_request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            results = data.get("query", {}).get("search", [])
            return [{"title": r["title"], "snippet": r.get("snippet", "")} for r in results]
        except Exception as e:
            _log('WIKI', f"search retry {attempt+1}/{retries} - {e}")
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    return []


def _wiki_extract(title, max_chars=1500, retries=3):
    """Get plain-text extract of Wikipedia article intro."""
    _step_counter['wiki_extract'] += 1
    params = urlencode({
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exintro": "true",
        "explaintext": "true",
        "exchars": max_chars,
        "format": "json",
    })
    url = f"{WIKI_API}?{params}"
    for attempt in range(retries):
        try:
            req = urllib_request.Request(url, headers={"User-Agent": "FACT-AUDIT-RAG/1.0"})
            with urllib_request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                extract = page.get("extract", "")
                if extract:
                    return extract.strip()
            return ""
        except Exception as e:
            _log('WIKI', f"extract retry {attempt+1}/{retries} - {e}")
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    return ""


def retrieve_wikipedia(claim, top_k=None, max_chars=None, delay=None):
    """Retrieve top-k Wikipedia passages relevant to a claim.

    Returns list of {text, source, score}.
    """
    top_k = top_k or WIKI_TOP_K
    max_chars = max_chars or WIKI_MAX_CHARS
    delay = delay if delay is not None else WIKI_DELAY

    _log('WIKI', f"Retrieving for: {claim[:80]}...")
    search_results = _wiki_search(claim, limit=top_k)
    evidence = []

    for i, result in enumerate(search_results):
        title = result["title"]
        extract = _wiki_extract(title, max_chars=max_chars)
        if not extract:
            extract = re.sub(r"<[^>]+>", "", result.get("snippet", ""))
        if not extract:
            continue

        evidence.append({
            "text": extract,
            "source": f"Wikipedia - {title}",
            "score": round(1.0 - (i * 0.1), 2),
        })

        if delay > 0 and i < len(search_results) - 1:
            time.sleep(delay)

    _log('WIKI', f"Retrieved {len(evidence)} passages")
    return evidence


# ============================================================
# Prompt Templates
# ============================================================

def gen_baseline_prompt(source_claim):
    """Baseline [claim] mode: only the source claim, no evidence."""
    return (
        'This is a fact-checking task. Please directly verify the factual accuracy '
        'of the statement provided below. Your response should conclude whether the '
        'statement in the question is Factual, Non-Factual, or Not Enough Information '
        'based on the claim itself.\n\n'
        f'Question: {source_claim}\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )


def gen_rag_prompt(source_claim, evidence_list):
    """RAG [evidence] mode: source claim + retrieved Wikipedia evidence."""
    evidence_block = ""
    for i, ev in enumerate(evidence_list, 1):
        source = ev.get("source", "Unknown")
        text = ev.get("text", "")
        evidence_block += f"\nEvidence {i} [{source}]:\n{text}\n"

    if not evidence_block:
        evidence_block = "\n(No relevant evidence found)\n"

    return (
        'This is a fact-checking task. Please verify the factual accuracy of the '
        'statement provided below using the attached evidence set. Your response should '
        'conclude whether the statement is Factual, Non-Factual, or Not Enough Information '
        'based on the evidence provided.\n\n'
        f'Source Claim: {source_claim}\n\n'
        f'Evidence Set:{evidence_block}\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )


# ============================================================
# Scoring (same judge as paper)
# ============================================================

def get_gpt4_score(question, answer, ref_ans, key_point):
    """Score LLaMA's answer against reference using GPT-4o-mini judge."""
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
    score_res = gpt4omini_turbo_generate(judge_prompt, temp=0)
    return score_res


def extract_score(score_text):
    """Extract numeric score from [[X]] format."""
    matches = re.findall(r'\[\[.*?\]\]', score_text.strip())
    if matches:
        try:
            return float(matches[-1].replace('[[', '').replace(']]', ''))
        except ValueError:
            pass
    return None


def gen_reference_answer(source_claim):
    """Generate reference answer using GPT-4o vote (3 answers → merge)."""
    prompt = gen_baseline_prompt(source_claim)
    _log('REF', "Generating 3 reference answers...")
    ref1 = gpt4o_turbo_generate(prompt, temp=0)
    ref2 = gpt4o_turbo_generate(prompt, temp=0)
    ref3 = gpt4o_turbo_generate(prompt, temp=0)

    vote_prompt = (
        'This is a fact-checking task. Please vote based on the three answers:\n'
        f'answer1 {ref1};\nanswer2 {ref2};\nanswer3 {ref3},\n'
        'and select the two most similar answers to merge. If the three answers conflict '
        'with each other, summarize the most appropriate answer based on the three answers. '
        'The output format should be consistent with the three answers. Your response should '
        'conclude whether the statement in the question is Factual, Non-Factual, or Not Enough '
        'Information.\n\n'
        f'Question: {source_claim}\n'
        'Answer: [Factual, Non-Factual, or Not Enough Information]\n'
        'Justification:'
    )
    _log('REF', "Voting on reference answers...")
    ref_ans = gpt4o_turbo_generate(vote_prompt, temp=0)
    return ref_ans


# ============================================================
# RAG Pipeline
# ============================================================

def run_single_claim(claim_data, idx, total):
    """Run baseline + RAG for a single claim, return comparison result."""
    source_claim = claim_data.get('source_claim', '')
    if isinstance(claim_data.get('prompt'), dict):
        source_claim = claim_data['prompt'].get('source_claim', source_claim)
    elif isinstance(claim_data.get('prompt'), str):
        source_claim = claim_data['prompt']

    key_point = claim_data.get('key_point', 'Verify factuality')
    test_mode = claim_data.get('test_mode', '[claim]')

    _log('CLAIM', f"[{idx}/{total}] {source_claim[:70]}...")
    _log('CLAIM', f"  key_point: {key_point} | original test_mode: {test_mode}")

    # Step 1: Generate reference answer (ground truth from GPT-4o)
    ref_ans = gen_reference_answer(source_claim)

    # Step 2: Baseline - LLaMA with claim only (no evidence)
    baseline_prompt = gen_baseline_prompt(source_claim)
    _log('BASELINE', "Calling LLaMA (claim-only)...")
    baseline_answer = llama_generate(baseline_prompt)

    # Step 3: RAG - Retrieve Wikipedia evidence, then LLaMA with evidence
    evidence = retrieve_wikipedia(source_claim)
    if evidence:
        rag_prompt = gen_rag_prompt(source_claim, evidence)
        _log('RAG', f"Calling LLaMA (with {len(evidence)} retrieved passages)...")
    else:
        rag_prompt = gen_baseline_prompt(source_claim)
        _log('RAG', "No evidence found, fallback to claim-only prompt...")
    rag_answer = llama_generate(rag_prompt)

    # Step 4: Score both answers
    _log('SCORE', "Scoring baseline...")
    baseline_score_text = get_gpt4_score(source_claim, baseline_answer, ref_ans, key_point)
    baseline_score = extract_score(baseline_score_text)

    _log('SCORE', "Scoring RAG...")
    rag_score_text = get_gpt4_score(source_claim, rag_answer, ref_ans, key_point)
    rag_score = extract_score(rag_score_text)

    result = {
        'claim_id': f"claim_{idx:03d}",
        'source_claim': source_claim,
        'key_point': key_point,
        'original_test_mode': test_mode,
        'reference_answer': ref_ans,
        'baseline': {
            'answer': baseline_answer,
            'score': baseline_score,
            'score_comment': baseline_score_text,
        },
        'rag': {
            'retrieved_evidence': evidence,
            'evidence_count': len(evidence),
            'answer': rag_answer,
            'score': rag_score,
            'score_comment': rag_score_text,
        },
        'improvement': (rag_score - baseline_score) if (rag_score and baseline_score) else None,
    }

    _log('RESULT', f"  Baseline={baseline_score} | RAG={rag_score} | Delta={result['improvement']}")
    return result


def load_claims_from_log(log_path):
    """Extract claims from a fact-audit log.json file."""
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    claims = []
    for key, value in data.items():
        if key in ('init_points', 'new_points', 'search_optimize_func', 'score_func', 'optimize_prompt'):
            continue
        if isinstance(value, dict):
            if 'seed_prompts' in value:
                for seed in value['seed_prompts']:
                    if isinstance(seed, dict) and ('prompt' in seed or 'source_claim' in seed):
                        claims.append(seed)
            if 'steps' in value:
                for step in value['steps']:
                    if isinstance(step, dict) and ('prompt' in step or 'source_claim' in step):
                        claims.append(step)
    return claims


def load_claims_from_category(category):
    """Generate seed claims for a category using the paper's gen_seed flow."""
    cat_file = '../data/fact_cat.json'
    if not os.path.exists(cat_file):
        _log('ERROR', f"Category file not found: {cat_file}")
        return []

    with open(cat_file, 'r') as f:
        categories = json.load(f)

    main_cat = category.lower().replace(' ', '_')
    if main_cat not in categories:
        _log('ERROR', f"Category '{main_cat}' not in fact_cat.json. Available: {list(categories.keys())}")
        return []

    points = categories[main_cat]
    task_name = f"{main_cat}:{points[0]}"
    _log('SEED', f"Generating seed claims for '{task_name}'...")

    # Simplified seed generation (just first point)
    prompt_template = """Fact-checking is an important capability of LLMs. Please generate 10 test cases for the "{task_name}" category covering different topics. Each test case should have a source_claim that can be fact-checked.

Output in JSON format: {"test_case1": {"key_point": "...", "test_mode": "[claim]", "prompt": {"source_claim": "...", "auxiliary_info": ""}}, "test_case2": {...}, ...}"""

    try:
        result = gpt4o_turbo_generate(prompt_template.replace("{task_name}", task_name), temp=0)
        match = re.search(r'({.*})', result, re.DOTALL)
        if match:
            parsed = json.loads(match.group(1))
            claims = []
            for k, v in parsed.items():
                if isinstance(v, dict) and 'prompt' in v:
                    claims.append(v)
            return claims
    except Exception as e:
        _log('ERROR', f"Seed generation failed: {e}")

    return []


def compute_metrics(results):
    """Compute paper metrics: IMR, JFR, Grade for both baseline and RAG."""
    baseline_scores = [r['baseline']['score'] for r in results if r['baseline']['score'] is not None]
    rag_scores = [r['rag']['score'] for r in results if r['rag']['score'] is not None]

    def _metrics(scores):
        if not scores:
            return {'grade': 0, 'imr': 0, 'count': 0}
        n = len(scores)
        grade = sum(scores) / n
        imr = sum(1 for s in scores if s <= 3) / n * 100
        return {'grade': round(grade, 2), 'imr': round(imr, 2), 'count': n}

    return {
        'baseline': _metrics(baseline_scores),
        'rag': _metrics(rag_scores),
        'improvements': [r['improvement'] for r in results if r['improvement'] is not None],
    }


def print_summary(metrics, results):
    """Print comparison summary table."""
    print("\n" + "=" * 70)
    print("FACT-AUDIT RAG Comparison Report")
    print("=" * 70)
    print(f"\nTotal claims evaluated: {len(results)}")
    print(f"LLaMA model: {TARGET_MODEL}")
    print(f"Wikipedia top-k: {WIKI_TOP_K}")
    print()

    print(f"{'Metric':<15} {'Baseline':>12} {'RAG':>12} {'Delta':>12}")
    print("-" * 53)

    b = metrics['baseline']
    r = metrics['rag']
    grade_delta = r['grade'] - b['grade']
    imr_delta = r['imr'] - b['imr']

    sign_g = "+" if grade_delta > 0 else ""
    sign_i = "+" if imr_delta > 0 else ""

    print(f"{'Grade (1-10)':<15} {b['grade']:>12.2f} {r['grade']:>12.2f} {sign_g}{grade_delta:>11.2f}")
    print(f"{'IMR (% <= 3)':<15} {b['imr']:>12.2f} {r['imr']:>12.2f} {sign_i}{imr_delta:>11.2f}")
    print(f"{'Count':<15} {b['count']:>12d} {r['count']:>12d}")

    improvements = metrics['improvements']
    if improvements:
        avg_imp = sum(improvements) / len(improvements)
        positive = sum(1 for i in improvements if i > 0)
        negative = sum(1 for i in improvements if i < 0)
        neutral = sum(1 for i in improvements if i == 0)
        print(f"\nPer-claim improvement: avg={avg_imp:+.2f}")
        print(f"  Improved: {positive}/{len(improvements)} | Degraded: {negative}/{len(improvements)} | Same: {neutral}/{len(improvements)}")

    print("\n" + "=" * 70)
    print(f"API calls: gpt4o={_step_counter['gpt4o']} mini={_step_counter['gpt4o_mini']} "
          f"llama={_step_counter['llama']} wiki_search={_step_counter['wiki_search']} "
          f"wiki_extract={_step_counter['wiki_extract']}")
    print("=" * 70)


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="FACT-AUDIT + RAG comparison pipeline")
    parser.add_argument('--input', type=str, default=None,
                        help="Path to existing log.json from a baseline fact-audit run")
    parser.add_argument('--category', type=str, default=None,
                        help="Generate fresh claims for this category (from fact_cat.json)")
    parser.add_argument('--limit', type=int, default=10,
                        help="Max claims to evaluate (default: 10)")
    parser.add_argument('--top-k', type=int, default=None,
                        help="Number of Wikipedia articles to retrieve (default: env WIKI_TOP_K or 5)")
    parser.add_argument('--max-chars', type=int, default=None,
                        help="Max chars per Wikipedia extract (default: env WIKI_MAX_CHARS or 1500)")
    parser.add_argument('--delay', type=float, default=None,
                        help="Delay between Wikipedia API calls in seconds (default: env WIKI_DELAY or 1.0)")
    parser.add_argument('--output', type=str, default=None,
                        help="Output JSON path (default: ../result/rag_comparison/)")
    args = parser.parse_args()

    # Override globals from args
    global WIKI_TOP_K, WIKI_MAX_CHARS, WIKI_DELAY
    if args.top_k:
        WIKI_TOP_K = args.top_k
    if args.max_chars:
        WIKI_MAX_CHARS = args.max_chars
    if args.delay is not None:
        WIKI_DELAY = args.delay

    # Load claims
    claims = []
    if args.input:
        _log('MAIN', f"Loading claims from: {args.input}")
        claims = load_claims_from_log(args.input)
    elif args.category:
        _log('MAIN', f"Generating claims for category: {args.category}")
        claims = load_claims_from_category(args.category)
    else:
        print("Error: Provide either --input (existing log.json) or --category")
        parser.print_help()
        return 1

    if not claims:
        _log('ERROR', "No claims loaded. Check input file or category name.")
        return 1

    # Apply limit
    claims = claims[:args.limit]
    _log('MAIN', f"Running RAG comparison on {len(claims)} claims")
    _log('MAIN', f"Config: top_k={WIKI_TOP_K}, max_chars={WIKI_MAX_CHARS}, delay={WIKI_DELAY}s")

    # Run pipeline
    results = []
    for idx, claim in enumerate(claims, 1):
        try:
            result = run_single_claim(claim, idx, len(claims))
            results.append(result)
        except Exception as e:
            _log('ERROR', f"Claim {idx} failed: {e}")
            continue

        # Save intermediate results
        if args.output:
            output_path = args.output
        else:
            output_dir = '../result/rag_comparison/'
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'rag_results.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'config': {
                    'llama_model': TARGET_MODEL,
                    'wiki_top_k': WIKI_TOP_K,
                    'wiki_max_chars': WIKI_MAX_CHARS,
                    'wiki_delay': WIKI_DELAY,
                    'total_claims': len(claims),
                },
                'results': results,
                'metrics': compute_metrics(results),
            }, f, indent=2, ensure_ascii=False)
        _log('SAVE', f"Saved {len(results)} results to {output_path}")

    # Final summary
    if results:
        metrics = compute_metrics(results)
        print_summary(metrics, results)

    return 0


if __name__ == '__main__':
    exit(main())
