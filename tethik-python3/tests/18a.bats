
@test "18a.py sample 1" {

input=$(cat << EOF
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
EOF
)

output=$(cat << EOF
4
EOF
)

result=$(echo "$input" | python 18a.py)
[[ "$result" == "$output" ]]
}



