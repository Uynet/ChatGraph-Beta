# スクリプト仕様

Exec ノードでは python コードを実行することができます。ChatGprah 上の多くのノードの正体は Exec ノードです。
詳しく調べたい方は以下のコードが参考になるでしょう。

- [debug](../src/debug/debugCommand.py)
- [thread](../src/api/threads.py)
- [execNode](../src/editors/models/nodes/execNode.py)

## 基本仕様
print 文による標準出力がノード終了時にDefaultソケットから出力されます。
エラー出力の場合Errorソケットからの出力になります。

## node

ローカル変数[node](https://github.com/Uynet/ChatGraph-Beta/blob/1eebafe0d0abd59fc2b9ebe41796c7126e23cdcf/src/debug/debugCommand.py#L23)によって自身の参照が渡されます。

### node.input

inputed への入力値を取得できます。これは実質的にnode.get("inputed")に等しいです。

### node.get

名前やアイコンなど、インスペクタで設定可能なノードのプロパティを取得できます。

```
name = node.get("label")
```

### node.set

- node.set("label","ノードの名前")
- node.set("icon","../images/customIcon.png")

存在しない property をセットしようとすると、**新たに追加されます。**
- [props](https://github.com/Uynet/ChatGraph-Beta/blob/1eebafe0d0abd59fc2b9ebe41796c7126e23cdcf/src/editors/types/dataType.py#L99)

### node.stream

print の他に、明示的に出力を行う方法を提供しています。

```
def stream(data:str ,isOutput = False , socket="Default"):
```

- data : str
  出力するテキストです。例：「こんにちは!」

- isOutput : bool
  False の場合、テキストフィールドの見た目のみ変更します。主に GPT ノード用です。
- socket : str
  出力ソケット名を指定します。If ノードで True/False で分岐するために使用されていますが、現状ソケット名はユーザーから変更できないため、この機能は無いと思ってよいでしょう。
