# Cloud9_Guest_Manager

- 指定のタグがついたcloud9開発環境の情報を収集する
- ゲストを紐付ける環境のリストを表示し、処理の続行を確認
- 環境の数に応じてゲスト用のIAMユーザーを作成する
  - 作成したIAMユーザーにはAWSCloud9EnvironmentMember管理ポリシーを紐付ける
- 各ゲストユーザーに開発環境のREAD-WRITE権限を与える
- 環境名、ユーザー名、ユーザーパスワードの情報を出力
  - コマンドラインに出力
  - csvに出力

## 参考

https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloud9/create-environment-membership.html
https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloud9/list-environments.html
https://awscli.amazonaws.com/v2/documentation/api/latest/reference/cloud9/describe-environments.html