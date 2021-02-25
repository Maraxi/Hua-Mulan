#/bin/sh

for i in "$@"
do
	case $i in
		-i)
			shift # past argument value
			input=$1
			shift
			;;
		-o)
			shift
			output=$1
			shift # past argument value
			;;
		*)
			# unknown option
			;;
	esac
done

echo "Reading from $input"
echo "Sending output to $output"

cd "$input"
cp "topics.xml" "/home/ul-t1-mulan/media/"
/snap/bin/docker-compose -f "/home/ul-t1-mulan/Hua-Mulan/Hua-Mulan/docker-compose.yml" up -d
sleep 60
# 5 runs
/snap/bin/docker exec python python evaluate.py -i /media -o /tmp -de args_original
#/snap/bin/docker exec python python evaluate.py -i /media -o /tmp -de args_t5expansion
#/snap/bin/docker exec python python evaluate.py -i /media -o /tmp -de args_gpt2expansion
#/snap/bin/docker exec python python evaluate.py -i /media -o /tmp -de args_naiveexpansion
#/snap/bin/docker exec python python evaluate.py -i /media -o /tmp -de args_original -qe 5
cd "$output"
cat "/home/ul-t1-mulan/Hua-Mulan/output/run.txt" >> "run.txt"
