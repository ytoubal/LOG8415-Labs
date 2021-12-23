package com.company;

import java.io.IOException;
import java.util.*;

import org.apache.commons.lang.mutable.MutableInt;
import org.apache.hadoop.io.Text;

public class Reducer extends org.apache.hadoop.mapreduce.Reducer<Text,FriendRelation,Text,Text> {

    public void reduce(Text key, Iterable<FriendRelation> values, Context context) throws IOException, InterruptedException {

        HashMap<String, MutableInt> friendsRecommendation = new HashMap(); //mix of users that are already friends and recommended friends
        ArrayList<String> currentFriends = new ArrayList(); //users that are already friend with the user key

        //Adding all the recommended friends and the number of mutual friends
        for (FriendRelation val : values) {

            if (val.relationship.get() == -1) { // already friends
                currentFriends.add(val.user.toString());

            } else if (!currentFriends.contains(val.user.toString())){ //potential friend

                MutableInt numMutualFriends = friendsRecommendation.get(val.user.toString());
                if (numMutualFriends == null) { // not in map already
                    friendsRecommendation.put(val.user.toString(), new MutableInt(1));
                } else { // already in map
                    numMutualFriends.increment();
                }
            }
        }

        //Sort the elements of the HashMap by their value (number of mutual friends)
        //inspired by https://stackoverflow.com/questions/2864840/treemap-sort-by-value
        Set<Map.Entry<String,MutableInt>> sortedMap = new TreeSet(
                new Comparator<Map.Entry<String,MutableInt>>() {
                    @Override public int compare(Map.Entry<String,MutableInt> e1, Map.Entry<String,MutableInt> e2) {
                        int res = e2.getValue().compareTo(e1.getValue());
                        int keyUser1 = Integer.parseInt(e1.getKey());
                        int keyUser2 = Integer.parseInt(e2.getKey());
                        return res != 0 ? res : Integer.compare(keyUser1,keyUser2); // Special fix to preserve items with equal values
                    }
                }
        );
        sortedMap.addAll(friendsRecommendation.entrySet());

        //Construct the final friend recommendation list
        int stopIndex = Math.min(sortedMap.size(), 10);
        int index = 0;
        StringBuilder recommendedFriends = new StringBuilder();
        String separator = "";

        for (Map.Entry<String, MutableInt> entry: sortedMap) {
            if (index == stopIndex)
                break;
            if (currentFriends.contains(entry.getKey())) //Ignore users that are already friend with the user key
                continue;

            recommendedFriends.append(separator).append(entry.getKey());
            separator = ",";
            index++;
        }

        context.write(key, new Text(recommendedFriends.toString()));
    }
}