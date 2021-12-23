/*
package com.company;

import java.io.IOException;
import java.lang.Math;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class PeopleYouMayKnow {

	public static void main(String ar[]) throws IOException, InterruptedException, ClassNotFoundException {

		Configuration conf = new Configuration();

		Job job1 = Job.getInstance(conf, "People_You_May_Know");
	    job1.setJarByClass(PeopleYouMayKnow.class);
	    job1.setMapperClass(Mapper.class);
	    job1.setReducerClass(Reducer.class);
		job1.setOutputKeyClass(Text.class);
		job1.setOutputValueClass(Text.class);

		Job job2 = Job.getInstance(conf, "People_You_May_Know_finish");
		job2.setMapperClass(Mapper2.class);
		job2.setReducerClass(Reducer2.class);
		job2.setOutputKeyClass(Text.class);
		job2.setOutputValueClass(Text.class);

	    //FileInputFormat.addInputPath(job, new Path(ar[0]));
		FileInputFormat.addInputPath(job1, new Path("/home/yanis/Desktop/PeopleYouMayKnow/soc-LiveJournal1Adj.txt"));
	    //FileOutputFormat.setOutputPath(job, new Path(ar[1]));
		String outputPath = "/home/yanis/Desktop/test/" + "10";
		FileOutputFormat.setOutputPath(job1, new Path(outputPath));
		job1.waitForCompletion(true);

		FileInputFormat.addInputPath(job2, new Path(outputPath));
		FileOutputFormat.setOutputPath(job2, new Path("/home/yanis/Desktop/test/11"));
	    System.exit(job2.waitForCompletion(true) ? 0 : 1);
	}
}
*/

package com.company;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class PeopleYouMayKnow {

	public static void main(String args[]) throws IOException, InterruptedException, ClassNotFoundException {

		Configuration conf = new Configuration();

		Job job = Job.getInstance(conf, "People_You_May_Know");
		job.setJarByClass(PeopleYouMayKnow.class);
		job.setMapperClass(Mapper.class);
		job.setReducerClass(Reducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FriendRelation.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
