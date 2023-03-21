## `GeomagQuickPlot`クラス
`GeomagQuickplot`クラスによりプロットを生成する。

```python
gq = GeomagQuickPlot()
gq.resolusion = 'min'　　 　　　　　　　　　　　　　　　　　　　　　　　　　　 # 1分値の場合'min'、1時間値の場合'hour'
gq.site_list = ['HON', 'ABG', HER']  # 観測地点の識別名称
gq.rootdir = 'aaa/bbb/ccc' # データファイルへのパス
gq.subdir = ['ddd', 'eee'] # データファイルへのパス（IDLのfilepath関数と同じ使い方）
gq.padvalue = 99999 # 欠損値の値、デフォルトでは9999
gq.unit = 50 # 各観測点ごとのプロットのパネルの高さをnT単位で指定する。
gq.linecolor = 'black' # ラインプロットの色
gq.t_start = datetime(2017, 5, 1) # プロットの開始時刻をdatetime型で与える。
gq.t_start = datetime(2017, 5, 10) # プロットの終了時刻をdatetime型で与える。
```
