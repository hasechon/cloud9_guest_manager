#!/bin/bash

num_user=$1
if expr "$num_user" : "[0-9]*$" >&/dev/null; then
    echo "ok"
else
    echo "$num_user is not number"
    exit 1
fi

echo $num_user

# IAMユーザー作成
list_user_name=("dummy")
for id_user in `seq -f '%03g' 1 $num_user`
do
    user_name=cloud9_guest_user_${id_user}
    list_user_name+=(${user_name})
    aws iam create-user --user-name ${user_name} >&/dev/null;
done

echo $list_user_name

echo "console login setting"
for i in `seq 1 $num_user`
do
    pwstr=$(pwgen -1n)
    echo $pwstr
    echo ${list_user_name[i]}
    aws iam create-login-profile --user-name ${list_user_name[i]} --password $pwstr --no-password-reset-required

    echo $i,${list_user_name[i]},$pwstr >> user_list.csv
done

echo "attach group"
for i in `seq 1 $num_user`
do
    # attach group
    echo $i
    echo ${list_user_name[i]}
    aws iam add-user-to-group --group-name cloud9_guest_group --user-name ${list_user_name[i]} 
done