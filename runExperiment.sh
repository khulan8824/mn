for i in 2 3 4
do
    rm -rf nohup.out
    nohup python random60nodes.py &
    echo "Running experiment"
    sleep 202m
done