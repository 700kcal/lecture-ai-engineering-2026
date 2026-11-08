# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0010050'), details={'text_prompt_tokens': 1550}, input_text_tokens=1550, input_tokens=1550, output_tokens=216, requests=2, tool_calls=2)
- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：追加したツール→make_quiz, save_leaming_log

## 宿題

- 取り組んだレベル：基礎
- やったこと： INSTRUCTIONS や docstring を変える
- 結果： INSTRUCTIONSを変更し質問をすると変更したことがすぐに反映されました。一方、docstringの変更はうまく反映できなかったように感じました。
- INSTRUCTIONSの変更点→①関係する回（第N回）のNの表示桁数を指定、②追加の説明を付け加えるように依頼
- docstiringの変更点→earch_glossaryを「query には調べたい用語をまとめて入れる。」に変更
- 気づき・疑問：
当初、実装の内容で取り組みましたが、うまく稼働しなかったため基礎の内容で提出することにしました。
実装でうまくいかなかった点は、ログを書くようにプログラムをcopilotに作ってもらい
保存するか聞かれるようにはなったのですが、ターミナルではこちらの返信を受け取れずログの書き込みもしないままでした。もう少し時間があれば追求したかったですが時間が足りず断念しました。

