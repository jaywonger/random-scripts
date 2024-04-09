#!/bin/sh 
#start mining ore auto restart when miner times out 
while true; 
do ore --rpc https://mainnet.helius-rpc.com/?api-key=e85f91af-6d72-4fd3-9268-f613156502e7 --keypair ~/.config/solana/id.json --priority-fee 50000 mine --threads 4
echo "stopped. restarting" 
sleep 1 
done