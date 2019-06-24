export PATH=$PATH:/usr/hdp/current/kafka-broker/bin
FILES=$1/*.txt
for f in $FILES
do
    echo "pushing $f file"
    cat $f | kafka-console-producer.sh --broker-list $2 --topic $3
    sleep 5
done
