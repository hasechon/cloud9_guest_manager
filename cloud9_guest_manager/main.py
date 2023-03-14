import subprocess
from subprocess import PIPE
import json
from typing import List, Optional
import time


def main():

    # 環境の情報を収集する

    out = exe_shell("aws cloud9 list-environments")

    print(out)
    print(type(out))

    list_env: Optional[List] = out.get("environmentIds")

    if list_env is None:
        return

    print(list_env)

    # タグでフィルタする

    # 確認
    print("continue?")
    while 1:
        user_response = input()
        if user_response == "y":
            break
        elif user_response == "n":
            return
        else:
            print("input y or n")

    # ゲストユーザー用のグループがなければ作成する

    # 環境の数だけユーザーを作成

    MEMBER_POLICY_ARN = "arn:aws:iam::aws:policy/AWSCloud9EnvironmentMember"
    list_user_arn = []
    for k, emv_id in enumerate(list_env):
        user_name = f"cloud9_guest_user_{k}"
        user_info = exe_shell(f"aws iam create-user --user-name {user_name}")
        user_arn = user_info["User"]["Arn"]

        while 1:
            out_flag = 0
            list_exist_users = exe_shell("aws iam list-users")

            for exist_user in list_exist_users["Users"]:
                if exist_user["UserName"] == user_name:
                    out_flag = 1
            if out_flag == 1:
                break

            print("wait 3 seconds")
            time.sleep(3)

        exe_shell(
            f"aws iam attach-user-policy --user-name {user_name} --policy-arn {MEMBER_POLICY_ARN}")

        time.sleep(3)

        # メンバーに追加
        cmd = f"aws cloud9 create-environment-membership --environment-id {emv_id} --user-arn {user_arn} --permissions read-write"
        exe_shell(cmd)
    return


def exe_shell(command: str) -> dict:
    proc = subprocess.run(command, shell=True,
                          stdout=PIPE, stderr=PIPE, text=True)
    print(proc.stdout)
    print(proc.stderr)
    if len(proc.stdout) != 0:
        out = json.loads(proc.stdout)
        return out

    return


def create_iam_user():
    pass


if __name__ == "__main__":
    main()
