# NicoCaptcha

　ニコニコ動画の会員登録時のCaptchaを自作ニューラルネットで突破した話です。いまはさらに強力なCaptchaになっているので、公開しても問題ないでしょう。

　文字の傾きを補正するために、重力の力学シミュレーションを使っているのがすこしユニークかもしれません。

## 説明スライド

　説明スライドはこちらにあります。

 - ニコニコ動画のCaptcha破ってみ…てる
   - http://www.slideshare.net/ledyba/captcha-10621422

## デモ

入力はこんな感じの文字列で：

![](https://raw.githubusercontent.com/ledyba/NicoCaptcha/master/image/1301.jpg)
![](https://raw.githubusercontent.com/ledyba/NicoCaptcha/master/image/1302.jpg)
![](https://raw.githubusercontent.com/ledyba/NicoCaptcha/master/image/1303.jpg)

前処理をしてニューラルネットに放り込んだ結果がこうなります：

![](https://raw.githubusercontent.com/ledyba/NicoCaptcha/master/image1.png)
