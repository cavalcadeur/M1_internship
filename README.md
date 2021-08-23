These files are supposed to be used as a library. You can also use main scripts to automatically run all the necessary analysis on a directory containing posts obtained via the youtube API or the CrowdTangle API.


Due to the requirements for the different python library. The scripts are split between the one using an older version of scikit and others using a more recent one.

The first script to use is pipeline.py

python3.6 pipeline.py -i directory/ --dir -p youtube -o output/result.csv     (to use with scikit-learn <= ???)

This will create a file summing up the posts stored in directory/. This script also runs a hate speech detection script and label each post.


The second script is update_database_bis.py

python3.8 update_database_bis.py -i output/database0.csv -o output/database1.csv -d topic -n 12

This creates a new file with more informations about the posts. It runs a Latent Dirichlet Allocation and label each post with a detected topic. The number of topics detected can be chosen with the parameter -n.

Another script can be used to add hope speech label to a database. This can be a bit slow to compute though.
