# Câu hỏi và câu trả lời phản biện

Tài liệu này tổng hợp các câu hỏi mà thầy hoặc các nhóm khác có thể đặt ra khi nhóm trình bày đề tài `FACT-AUDIT + RAG`, kèm theo câu trả lời gợi ý chi tiết hơn để nhóm dễ luyện nói và ứng biến.

## 1. `FACT-AUDIT` khác gì với các benchmark fact-checking truyền thống dùng dataset tĩnh?

Điểm khác biệt lớn nhất là `FACT-AUDIT` không đánh giá mô hình trên một bộ dữ liệu kiểm thử cố định, mà dùng cơ chế sinh test case động và cập nhật dần theo điểm yếu của mô hình đang được đánh giá. Với benchmark truyền thống, cùng một bộ câu hỏi sẽ được dùng lặp đi lặp lại cho nhiều mô hình, nên về lâu dài có nguy cơ rò rỉ dữ liệu kiểm thử, khiến mô hình vô tình hoặc trực tiếp “học thuộc” dạng bài kiểm tra. Khi đó, điểm số cao chưa chắc phản ánh năng lực fact-checking thật sự.

Còn với `FACT-AUDIT`, framework vận hành theo kiểu thích nghi. Sau mỗi vòng, hệ thống nhìn vào những lỗi mà mô hình vừa mắc phải, rồi tiếp tục sinh thêm các case khó hơn hoặc đúng vào vùng mô hình còn yếu. Vì vậy, bài đánh giá trở nên “sống”, bám vào hành vi thực tế của mô hình thay vì chỉ chấm nó trên một đề thi cố định. Ngoài ra, `FACT-AUDIT` còn đánh giá cả phần lập luận `justification`, trong khi nhiều benchmark cũ chủ yếu chỉ chấm nhãn đúng hay sai.

## 2. Vì sao bài báo không chỉ đo `accuracy` của verdict mà còn phải chấm cả `justification`?

Vì trong bài toán fact-checking, việc mô hình đưa ra nhãn đúng chưa đủ để kết luận là mô hình đáng tin. Một mô hình có thể trả lời đúng nhãn `Đúng`, `Sai`, hoặc `Chưa đủ thông tin`, nhưng phần giải thích lại hời hợt, suy luận sai, hoặc dùng bằng chứng không phù hợp. Nếu chỉ nhìn vào accuracy của verdict, ta có thể đánh giá quá cao những mô hình “đoán đúng” nhưng không thật sự hiểu vấn đề.

Phần `justification` rất quan trọng vì nó phản ánh chất lượng suy luận. Trong thực tế, khi dùng hệ thống fact-checking, người dùng không chỉ muốn biết kết quả cuối cùng mà còn muốn hiểu vì sao hệ thống lại kết luận như vậy. Nếu giải thích sai, thì ngay cả khi verdict đúng ở một vài trường hợp, mô hình vẫn có thể gây mất niềm tin hoặc dẫn người dùng đến những kết luận sai trong các trường hợp khác. Vì vậy, paper nhấn mạnh rằng fact-checking là nhiệm vụ vừa cần kết luận đúng vừa cần lập luận đúng.

## 3. Chỉ số `IMR` và `JFR` phản ánh điều gì, và vì sao cần cả hai thay vì chỉ giữ một chỉ số?

`IMR` là viết tắt của `Insight Mastery Rate`, dùng để đo tỷ lệ các test case mà mô hình thất bại nghiêm trọng, cụ thể là những case bị chấm `Grade <= 3`. Chỉ số này cho biết mô hình có thường xuyên mắc lỗi nặng hay không. Nếu `IMR` thấp, điều đó nghĩa là mô hình ít rơi vào các tình huống trả lời kém chất lượng.

`JFR` là `Justification Flaw Rate`, đo tỷ lệ trường hợp mô hình đưa ra verdict đúng nhưng justification lại có vấn đề. Đây là chỉ số rất quan trọng vì nó bóc tách riêng một kiểu lỗi khá nguy hiểm: bề ngoài mô hình có vẻ đúng, nhưng thực chất phần giải thích không đáng tin. Nếu chỉ dùng `IMR` hoặc accuracy, ta sẽ khó nhìn ra những lỗi kiểu này.

Nói ngắn gọn, `IMR` giúp đo mức độ thất bại tổng quát và nghiêm trọng, còn `JFR` giúp phát hiện những lỗi “ẩn” trong phần lập luận. Hai chỉ số bổ sung cho nhau để tạo ra cái nhìn đầy đủ hơn về năng lực fact-checking của mô hình.

## 4. Tại sao mốc `Grade <= 3` lại được dùng để xác định một case là thất bại?

Trong rubric chấm điểm của paper, thang điểm `Grade` chạy từ 1 đến 10. Tuy nhiên, paper quy ước khá rõ rằng nếu mô hình sai ở verdict hoặc phần justification có lỗi nghiêm trọng, thì bài trả lời đó không thể được chấm quá 3 điểm. Vì vậy, ngưỡng `3` trở thành một ranh giới tự nhiên để tách các câu trả lời thất bại ra khỏi các câu trả lời còn chấp nhận được.

Việc dùng ngưỡng này có hai lợi ích. Thứ nhất, nó giúp chuyển thang điểm liên tục thành một chỉ báo dễ tổng hợp, từ đó tính ra `IMR`. Thứ hai, nó khiến việc đánh giá bớt mơ hồ hơn, vì thay vì tranh luận giữa mức 5 hay 6, paper tập trung vào việc một câu trả lời có rơi vào nhóm lỗi nặng hay không. Khi trình bày, nhóm có thể nói rằng đây là ngưỡng operational do paper đặt ra để đo tỷ lệ thất bại nghiêm trọng một cách nhất quán.

## 5. `Importance Sampling` trong framework này giúp gì hơn so với lấy mẫu ngẫu nhiên thông thường?

Nếu dùng lấy mẫu ngẫu nhiên thông thường, hệ thống sẽ phải tạo ra rất nhiều test case trước khi tình cờ chạm vào đúng những vùng mà mô hình thực sự yếu. Điều này vừa tốn tài nguyên, vừa làm tốc độ hội tụ chậm. `Importance Sampling` giải quyết vấn đề đó bằng cách phân bổ nhiều xác suất hơn cho những vùng được dự đoán là “khó” hoặc có giá trị đánh giá cao hơn.

Trong ngữ cảnh của `FACT-AUDIT`, ý tưởng là sau khi quan sát các lỗi trước đó của mô hình, framework sẽ ưu tiên sinh thêm các câu hỏi cùng loại hoặc các biến thể gần với vùng lỗi đó. Như vậy, nó không khám phá không gian test case một cách dàn đều, mà tập trung đào sâu vào đúng chỗ mô hình có nguy cơ sai. Kết quả là framework phát hiện điểm yếu nhanh hơn, đánh giá sắc hơn, và dùng ít mẫu hơn để đạt được mức hiểu tương đương.

## 6. Vì sao framework phải dùng tới `5 agent`, liệu có quá phức tạp không?

Thoạt nhìn, việc dùng `5 agent` có vẻ khá phức tạp, nhất là nếu so với cách đánh giá truyền thống chỉ cần một bộ dữ liệu và một script chấm điểm. Tuy nhiên, mỗi agent trong `FACT-AUDIT` đảm nhiệm một vai trò riêng và giúp pipeline trở nên mô-đun hơn.

`Appraiser` xây dựng và cập nhật cây kịch bản. `Inquirer` sinh ra các test case cụ thể. `Quality Inspector` kiểm tra chất lượng và độ đa dạng của dữ liệu, đồng thời đối chiếu thông tin với nguồn đáng tin như Wikipedia. `Evaluator` đóng vai trò judge để chấm verdict và justification. `Prober` phân tích bộ nhớ lỗi trước đó để tạo ra các case mới khó hơn. Việc tách vai như vậy giúp hệ thống rõ trách nhiệm hơn, dễ thay thế từng thành phần, và quan trọng nhất là hỗ trợ cơ chế đánh giá lặp thích nghi.

Vì vậy, có thể nói framework này phức tạp hơn benchmark tĩnh, nhưng sự phức tạp đó là có chủ đích. Nó đổi lấy khả năng đánh giá sâu hơn, tự động hơn và sát với điểm yếu thật của mô hình hơn.

## 7. Agent `Evaluator` là một LLM khác đóng vai judge; vậy làm sao đảm bảo việc chấm điểm không bị thiên lệch?

Đây là một câu hỏi rất hay và cũng là một điểm mà nhóm nên chủ động thừa nhận. Khi dùng một LLM khác để làm judge, chắc chắn sẽ tồn tại nguy cơ thiên lệch hoặc không ổn định trong chấm điểm. Paper giảm bớt rủi ro đó bằng cách thiết kế rubric chấm điểm tương đối rõ, yêu cầu judge đánh giá nhất quán cả verdict lẫn justification, và áp dụng cùng một quy trình cho tất cả mô hình được test.

Tuy nhiên, nói một cách công bằng thì framework này không loại bỏ hoàn toàn thiên lệch của judge. Thay vào đó, nó chấp nhận một trade-off: dùng LLM-as-a-Judge để đổi lấy khả năng tự động hóa ở quy mô lớn. Khi trả lời, nhóm có thể nói rằng độ tin cậy của kết quả phụ thuộc một phần vào chất lượng của judge, nên về thực tế, một hướng cải tiến quan trọng là dùng nhiều judge, kiểm tra độ đồng thuận, hoặc hiệu chỉnh judge bằng tập đối chiếu do con người gán nhãn.

## 8. Nếu judge model chấm sai hoặc không ổn định thì toàn bộ kết quả có bị ảnh hưởng không?

Có, và ảnh hưởng này là đáng kể, vì toàn bộ các chỉ số như `Grade`, `IMR`, và `JFR` đều được xây dựng từ quá trình chấm của `Evaluator`. Nếu judge quá dễ hoặc quá nghiêm, kết quả cuối cùng có thể bị lệch theo một hướng nào đó. Tệ hơn, nếu judge không ổn định giữa các lần chạy, thì độ tin cậy và khả năng tái lập của benchmark cũng giảm.

Tuy vậy, điều này không có nghĩa là framework mất giá trị. Nó chỉ cho thấy rằng `Evaluator` là một điểm trọng yếu cần được kiểm soát. Khi phản biện, nhóm có thể nói rằng đây là hạn chế nội tại của các hệ thống đánh giá tự động dùng LLM judge. Cách khắc phục trong tương lai có thể là dùng nhiều judge độc lập, tính agreement giữa các judge, hoặc dùng thêm đánh giá con người trên một tập nhỏ để hiệu chuẩn kết quả.

## 9. Điểm mạnh lớn nhất của `FACT-AUDIT` so với human annotation là gì, và điểm yếu lớn nhất là gì?

Điểm mạnh lớn nhất là khả năng tự động hóa và mở rộng quy mô. Nếu dùng human annotation thuần túy, chi phí gán nhãn sẽ rất cao, thời gian chậm, và khó cập nhật liên tục khi mô hình mới xuất hiện. `FACT-AUDIT` giúp sinh test case, chấm điểm, và đào sâu điểm yếu theo vòng lặp gần như hoàn toàn tự động, nên phù hợp với bối cảnh LLM thay đổi rất nhanh.

Ngoài ra, framework còn có ưu điểm là đánh giá thích nghi theo từng mô hình, điều mà human annotation trên dataset tĩnh thường không làm được. Tuy nhiên, điểm yếu lớn nhất là độ tin cậy của toàn hệ thống vẫn phụ thuộc vào các agent nền, đặc biệt là judge và thành phần kiểm chứng evidence. Nói cách khác, human annotation mạnh ở độ chắc chắn cục bộ, còn `FACT-AUDIT` mạnh ở quy mô, tốc độ và khả năng cập nhật. Đây là hai hướng có thể bổ trợ nhau chứ không hoàn toàn thay thế nhau.

## 10. Vì sao paper nói framework này `model-centric` và `adaptive`?

Paper gọi framework là `model-centric` vì toàn bộ quá trình đánh giá được xoay quanh hành vi của mô hình đang được test, chứ không chỉ áp một bộ đề chung cho mọi mô hình. Sau mỗi vòng, framework nhìn vào những lỗi mà chính mô hình đó mắc phải để quyết định nên sinh thêm loại câu hỏi nào. Điều này khiến bài đánh giá trở nên cá nhân hóa theo từng mô hình.

Từ đó xuất hiện tính `adaptive`. Framework không đứng yên mà cập nhật liên tục. Nếu mô hình yếu ở suy luận nhiều bước, hệ thống sẽ đẩy thêm các case thuộc vùng đó. Nếu mô hình hay sai khi xử lý tin đồn mạng xã hội, framework sẽ mở rộng các tình huống tương ứng. Vậy nên “adaptive” ở đây không chỉ là cập nhật dữ liệu, mà là cập nhật có định hướng dựa trên lịch sử lỗi.

## 11. Trong 3 nhóm kịch bản `Complex Claim`, `Fake News`, `Social Rumor`, nhóm nào khó nhất và vì sao?

Theo phần phân tích trong slide, nhóm `Complex Claim` thường là khó nhất vì nó đòi hỏi mô hình thực hiện suy luận nhiều bước thay vì chỉ đối chiếu một fact đơn lẻ. Với kiểu bài này, mô hình không chỉ cần nhớ kiến thức mà còn phải nối được nhiều mảnh thông tin lại với nhau theo một chuỗi logic. Đây là nơi các lỗi suy luận dễ lộ ra nhất.

`Fake News` và `Social Rumor` cũng khó, nhưng độ khó thường đến từ kiểu nhiễu thông tin, tiêu đề đánh lạc hướng, hoặc hiệu ứng cảm xúc, kỳ vọng, sợ hãi trong phát ngôn cộng đồng. Còn `Complex Claim` thì trực diện thử năng lực reasoning. Vì vậy nếu bị hỏi nhóm nào khó nhất, nhóm có thể trả lời rằng theo paper và theo logic bài toán, `Complex Claim` là nhóm bộc lộ rõ hạn chế suy luận nhất.

## 12. Tại sao `Test Mode` có evidence lại cho kết quả tốt hơn nhiều so với claim-only mode?

Khi ở `claim-only mode`, mô hình phải dựa gần như hoàn toàn vào tri thức nội tại đã học trong quá trình pretraining. Nếu kiến thức cũ, thiếu, hoặc bị lẫn, mô hình rất dễ hallucinate hoặc đưa ra kết luận sai. Ngược lại, khi có `evidence`, mô hình được cung cấp thêm căn cứ bên ngoài để đối chiếu claim, nên giảm phụ thuộc vào trí nhớ bên trong và tăng khả năng fact-check đúng.

Điều này cũng phù hợp với trực giác thực tế: một người có tài liệu tham khảo trước mặt thường kiểm chứng tốt hơn là chỉ nhớ bằng đầu. Kết quả paper cho thấy mode có evidence làm giảm `IMR` rõ rệt, từ đó chứng minh rằng chất lượng và sự sẵn có của bằng chứng là yếu tố cực kỳ quan trọng trong bài toán fact-checking.

## 13. Nếu đã có mode `evidence`, vậy `RAG` mà nhóm đề xuất khác gì với việc chỉ đưa “gold evidence” cho mô hình?

`Gold evidence` là bằng chứng lý tưởng, nghĩa là bằng chứng đã được chọn sẵn, đúng, sạch, và phù hợp trực tiếp với claim. Vì vậy, mode này giống như một “trần trên” để cho thấy nếu mô hình được cung cấp evidence hoàn hảo thì nó có thể làm tốt đến đâu. Nhưng trong ứng dụng thực tế, hệ thống không có sẵn gold evidence như vậy.

`RAG` khác ở chỗ nó phải tự đi truy hồi tài liệu từ một kho tri thức hoặc từ web. Vì vậy, chất lượng đầu ra sẽ phụ thuộc mạnh vào retriever: truy hồi có đúng tài liệu không, có đủ thông tin không, có bị nhiễu không, có lấy trúng đoạn liên quan nhất không. Nói cách khác, `gold evidence` là điều kiện lý tưởng, còn `RAG` là cách đưa bài toán đến gần bối cảnh triển khai thật. Nếu retriever tốt, hiệu năng có thể tiến gần mode `evidence`; nếu retriever kém, hệ thống có thể chỉ tốt hơn `claim-only` một phần.

## 14. Trong phần reproduction của nhóm, kết quả có khớp hoàn toàn với paper không? Nếu lệch thì nguyên nhân có thể là gì?

Thông thường, rất khó để reproduction khớp hoàn toàn với paper, đặc biệt là với các bài làm trên nền LLM API. Có nhiều nguyên nhân dẫn đến sai khác: phiên bản model có thể đã thay đổi theo thời gian, hành vi API không cố định tuyệt đối, prompt implementation của nhóm có thể khác một chút so với bản gốc, hoặc nguồn evidence truy xuất được ở thời điểm chạy lại không giống hệt paper.

Ngoài ra, ngay cả khi nhiệt độ bằng 0, một số khác biệt kỹ thuật nhỏ trong preprocessing, parsing, hoặc cách triển khai agent cũng có thể làm kết quả lệch đi. Khi trả lời câu này, nhóm nên nhấn mạnh rằng mục tiêu của reproduction không nhất thiết là lặp lại y hệt từng con số, mà là kiểm tra xem xu hướng chính của paper có còn giữ được hay không, ví dụ như mode có evidence tốt hơn claim-only, hay một số nhóm kịch bản khó hơn rõ rệt.

## 15. Nếu triển khai thực tế, nhóm sẽ chọn cải thiện phần nào trước: retriever, judge, hay taxonomy kịch bản?

Nếu mục tiêu là biến hệ thống thành một pipeline có giá trị sử dụng thực tế, nhóm nên ưu tiên cải thiện `retriever` trước. Lý do là chất lượng evidence đầu vào ảnh hưởng trực tiếp đến chất lượng fact-checking. Nếu tài liệu truy hồi sai hoặc nhiễu, ngay cả một mô hình mạnh cũng khó đưa ra verdict và justification đúng.

Sau retriever, thành phần nên ưu tiên tiếp theo là `judge`, vì judge quyết định độ tin cậy của phần đánh giá. Nếu đánh giá không ổn định, ta rất khó biết cải tiến nào là thật sự hiệu quả. Cuối cùng mới là mở rộng `taxonomy` để bao phủ thêm nhiều loại tình huống. Nói ngắn gọn: evidence tốt là nền tảng, judge tốt là công cụ đo, còn taxonomy rộng là bước hoàn thiện để benchmark bao quát hơn.

## 16. Tại sao nhóm nói đây là framework đánh giá năng lực fact-checking, chứ không phải hệ thống fact-checking hoàn chỉnh?

Điểm cốt lõi là `FACT-AUDIT` được thiết kế trước hết để đo và phân tích năng lực của mô hình, chứ không phải để triển khai như một sản phẩm fact-checking cho người dùng cuối. Các agent trong framework chủ yếu phục vụ việc sinh đề, chấm điểm, phát hiện điểm yếu, và cập nhật bài kiểm tra. Nói cách khác, mục tiêu của nó là “đo lường”, không phải “phục vụ trực tiếp người dùng”.

Một hệ thống fact-checking hoàn chỉnh trong thực tế còn cần thêm nhiều thành phần khác như truy hồi tài liệu thời gian thực, giao diện giải thích cho người dùng, kiểm soát nguồn tin, logging, và cơ chế giám sát rủi ro. `FACT-AUDIT` có thể là nền tảng rất tốt để đánh giá những hệ thống như vậy, nhưng bản thân nó không phải là toàn bộ sản phẩm cuối.

## 17. Nếu một mô hình có verdict đúng nhưng justification yếu, điều đó có nghiêm trọng không?

Theo nhóm, điều này vẫn khá nghiêm trọng. Trong fact-checking, một verdict đúng nhưng justification yếu có thể tạo cảm giác mô hình “đúng”, nhưng thực ra nó không cho thấy năng lực suy luận đáng tin. Nếu sau này gặp một trường hợp khó hơn, mô hình đó có thể đổi sang verdict sai mà người dùng vẫn khó nhận ra, vì nó vốn không có nền tảng giải thích chắc chắn.

Ngoài ra, trong ứng dụng thực tế, người dùng thường cần lý do để tin vào kết quả. Nếu justification mơ hồ hoặc sai lệch, hệ thống sẽ khó được chấp nhận trong các bối cảnh nhạy cảm như giáo dục, truyền thông, hay hỗ trợ ra quyết định. Vì vậy, paper mới tách riêng `JFR` để đo chính loại lỗi này.

## 18. Hướng mở rộng với `RAG` của nhóm có ý nghĩa gì về mặt nghiên cứu?

Hướng mở rộng này có ý nghĩa ở chỗ nó nối benchmark của paper với bối cảnh triển khai thực tế hơn. Paper đã chỉ ra rằng khi có evidence, hiệu năng fact-checking tăng lên đáng kể. Từ đó, nhóm đề xuất `RAG` như một cơ chế để cung cấp evidence động thay vì chỉ dựa vào trí nhớ nội tại của mô hình.

Về mặt nghiên cứu, điều này mở ra câu hỏi rất hay: hiệu năng fact-checking thực tế phụ thuộc bao nhiêu phần vào bản thân LLM, và bao nhiêu phần vào chất lượng truy hồi evidence? Nếu sau này nhóm đo được sự thay đổi `IMR` hoặc `JFR` khi thay retriever, thì đó sẽ là một đóng góp thú vị vì nó tách riêng được ảnh hưởng của từng thành phần trong pipeline.

## Ghi chú luyện nói

- Các câu trả lời trên được viết theo hướng đủ chi tiết để bạn rút ý khi nói.
- Khi trình bày miệng, nên nén mỗi câu còn khoảng 3 ý chính để tránh trả lời quá dài.
- Có thể chia người trả lời theo phần:
- Tiến: bối cảnh, động lực, framework, importance sampling.
- Quang: 5 agent, metrics, kết quả, test mode.
- Ấn: reproduction, RAG, hướng mở rộng và ứng dụng thực tế.
