echo 'how many extra datanodes do you want for the data analytics(there is already 1)'
read numberofnodes

python updatestack.py $numberofnodes