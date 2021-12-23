# WordCount on Hadoop

Running the code with the jar file is the easiest way to run the code without even needing Hadoop configured in the environment. The only requirement is Java to run the jar file and a Linux Distribution. 

The jar file is located in the HadoopWordCount/out/artifacts/HadoopWordCount_jar/ directory and the command to run it is simply:

java -jar HadoopWordCount.jar path/to/input/file path/to/output/directory

# WordCount on Spark

=> The first step is to install Spark 3.2.0 and maven package

=> Second step is to create a directory (/home/ubuntu/SparkDir/sparkwordcount/com/tp2/wordcount) where SparkWordCount.scala program will be

=> Then copy paste the pom.xml file in /sparkwordcount and generate the application jar by running "mvn package" command from that same directory. Note: this will generate sparkwordcount-0.0.1-SNAPSHOT.jar in /target directory (~/sparkwordcount/target)

=> Launch the SparkWordCount.scala script from its directory (~/tp2/wordcount) by typing the following command:
     spark-submit --class SparkWordCount $YOUR_LINK/target/sparkwordcount-0.0.1-SNAPSHOT.jar $YOUR_LINK/YOURFILE.txt

# People You May Know

Running the code with the jar file is the easiest way to run the code without even needing Hadoop configured in the environment. The only requirement is Java to run the jar file and a Linux environment. 

The jar file is located in the PeopleYouMightKnow/out/artifacts/PeopleYouMayKnow_jar/ directory and the command to run it is simply:

java -jar PeopleYouMayKnow.jar path/to/input/file path/to/output/directory
