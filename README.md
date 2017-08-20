# PWM_Account_view_tracking
PWM日本証券のアカウントビューに表示される当日の価格データの一部をcsvファイルに出力するスクリプト

# raspberrypiへの構築方法について
## raspbianのインストール
以下のimageをダウンロードしてraspberrypiにインストールする。
http://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2017-07-05/2017-07-05-raspbian-jessie-lite.zip
※以下で使用するansible-playbookは上記imageにしか対応していない。

`sudo raspi-config`でsshを有効化する。

`sudo passwd`でrootのパスワードを設定する。

/etc/ssh/sshd_configを修正して、sshのrootパスワードログインを許可する。

## 設定ファイルを用意する
ansible/hosts_sampleをansible/hostsに名称変更する。

hostsに記載されているipをraspberrypiのipに書き換える
```
[raspberrypi]
192.168.0.10
```
group_vars/all_sample.yamlをgroup_vars/all.yamlに名称変更する。

all.yamlの内容を、記載されているコメントにそって編集する。

## ansible-playbookを実行する
ansibleディレクトリにて、`ansible-playbook -k -i hosts init_raspberrypi.yaml`を実行する。

完了したら続いて`ansible-playbook -K -i hosts pwm_setting.yaml`を実行する。

# データ取得について
データはdata/data.csvに保存される。  
データ取得は毎日22:15に実行される。  
すでに同日データが存在する場合（例えば日曜日に実行された場合、取得されるデータは金曜日のもので、すでに取得されているはず）はデータ追記されない。
