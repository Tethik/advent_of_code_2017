
@test "18b.py sample 1" {

input=$(cat << EOF
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
EOF
)

output=$(cat << EOF
3
EOF
)

result=$(echo "$input" | python 18b.py)
[[ "$result" == "$output" ]]
}



