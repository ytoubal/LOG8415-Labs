package com.company;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

public class Mapper extends org.apache.hadoop.mapreduce.Mapper<LongWritable, Text, Text, FriendRelation> {

	Text userId;
	String[] userFriends;
	String[] userEntry;
	final IntWritable already_friends = new IntWritable(-1);
	final IntWritable potentially_not_friends = new IntWritable(1);

	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

		//Separating the key and the value from the input
		userEntry = value.toString().split("\\s");
		if (userEntry.length == 1)
			return;
		userId = new Text(userEntry[0]);
		userFriends = userEntry[1].split(",");

		for (int i = 0; i < userFriends.length; ++i) {
			Text friend = new Text(userFriends[i]);
			context.write(userId, new FriendRelation(friend, already_friends)); // is already a friend of the user

			//Create all the unique permutation pairs between the friends of the user
			//Inspired by https://stackoverflow.com/questions/35734388/print-unique-permutations-of-pairs-from-an-array
			for (int j = i+1; j < userFriends.length; ++j) {
				Text anotherFriend = new Text(userFriends[j]);
				context.write(friend, new FriendRelation(anotherFriend, potentially_not_friends));
				context.write(anotherFriend, new FriendRelation(friend, potentially_not_friends));
			}
		}
	}
}