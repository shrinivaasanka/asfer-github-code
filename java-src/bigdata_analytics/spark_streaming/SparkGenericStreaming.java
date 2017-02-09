/*
#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------
*/

/*
Reference:
----------
Java Spark Streaming Examples - http://spark.apache.org/docs/latest/streaming-programming-guide.html
*/

/*
Custom Receiver for generic stream data - URL and sockets
*/

import java.util.Arrays;
import java.util.Iterator;
import java.util.regex.Pattern;

import scala.Tuple2;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFunction;
import org.apache.spark.api.java.StorageLevels;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;

import org.apache.spark.storage.StorageLevel;
import org.apache.spark.streaming.Duration;
import org.apache.spark.streaming.receiver.Receiver;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public final class SparkGenericStreaming extends Receiver<String> {
  private static final Pattern SPACE = Pattern.compile(" ");
  String urlargs = "localhost";
  String host = "localhost";
  static boolean isURLsocket=true;
  static boolean useJsoup=true;
  int port = 80;
  static SparkConf sparkConf;
  static JavaStreamingContext ssc;

  public SparkGenericStreaming(String url) {
	super(StorageLevel.MEMORY_AND_DISK_2());
	this.urlargs = url;
  }

  public SparkGenericStreaming(String hst, int prt) {
	super(StorageLevel.MEMORY_AND_DISK_2());
	host = hst;
	port = prt;
  }

  public void onStart() {
	System.out.println("SparkGenericStreaming Receiver Started");
	new Thread() {
		@Override
		public void run() {
			receive();
		}
	}.start();
  }

  public void onStop() {
	System.out.println("SparkGenericStreaming Receiver Stopped");
  }

  public void receive() {
	if (isURLsocket)
	{
		if(useJsoup)
		{
			while(true)
			{
				try 
				{
					Document doc = 	Jsoup.connect(urlargs).get();
					String text = doc.body().text();
					//System.out.println("JSoup ETL: text:"+text);
					store(text);
				}
				catch (Exception e)
				{
					System.out.println("Exception:" + e);
				}
			}
		}
		else
		{
			URL url = null;
			HttpURLConnection conn = null;
			BufferedReader br = null;
			String input;
			while(true)
			{
				try{
					url = new URL(urlargs);
					conn = (HttpURLConnection) url.openConnection();
					conn.setRequestMethod("GET");
					//conn.setDoOutput(true);
					br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
					while((input=br.readLine()) != null)
					{
						//System.out.println("Streaming data received:"+input);
						store(input);
					}
				} catch (Exception e) {
					System.out.println("Exception:" + e);
				}
			}
		}
	}
	else
	{
		Socket s = null;
		BufferedReader br = null;
		String input;
		try{
			s = new Socket(host,port);
			br = new BufferedReader(new InputStreamReader(s.getInputStream()));
			while(!isStopped() && (input=br.readLine()) != null)
			{
				System.out.println("Streaming data received:"+input);
				store(input);
			}
		} catch (Exception e) {
			System.out.println("Exception:" + e);
		}
	}
  }

  public JavaPairDStream<String,Integer> SparkGenericStreamingMain(String[] args) throws Exception {
    if (args.length > 2) {
     System.err.println("Usage: SparkGenericStreaming <url> (or) SparkGenericStreaming <host> <port>");
     System.exit(1);
    }

    // Create the context with a 5 second batch size
    //SparkConf sparkConf = new SparkConf().setAppName("SparkGenericStreaming");
    sparkConf = new SparkConf().setAppName("SparkGenericStreaming");
    ssc = new JavaStreamingContext(sparkConf, Durations.seconds(5));
    ssc.sparkContext().setLogLevel("ERROR");

    // Create a JavaReceiverInputDStream on target ip:port and count the
    // words in input stream of \n delimited text (eg. generated by 'nc')
    // Note that no duplication in storage level only for running locally.
    // Replication necessary in distributed scenario for fault tolerance.
    
    JavaReceiverInputDStream<String> lines;
    if(SparkGenericStreaming.isURLsocket)
    {
	lines = ssc.receiverStream(new SparkGenericStreaming(args[0]));
    }
    else
    {
	lines = ssc.receiverStream(new SparkGenericStreaming(args[0], Integer.parseInt(args[1])));
    }

    JavaDStream<String> words = lines.flatMap(new FlatMapFunction<String, String>() {
      @Override
      public Iterator<String> call(String x) {
        return Arrays.asList(SPACE.split(x)).iterator();
      }
    });
    
    JavaPairDStream<String, Integer> wordCounts = words.mapToPair(
     new PairFunction<String, String, Integer>() {
        @Override
        public Tuple2<String, Integer> call(String s) {
          return new Tuple2<>(s, 1);
        }
      }).reduceByKey(new Function2<Integer, Integer, Integer>() {
        @Override
        public Integer call(Integer i1, Integer i2) {
          return i1 + i2;
        }
      });

    //words.print();
    //wordCounts.print();
    //wordCounts.foreachRDD(x->{ x.collect().stream().forEach(y->System.out.println(y)); });
    //ssc.start();
    //ssc.awaitTermination();
    return wordCounts;
  }
  
  public static void main(String[] args) throws Exception {
	SparkGenericStreaming sgs;
	if(SparkGenericStreaming.isURLsocket)
		sgs = new SparkGenericStreaming(args[0]);
	else
		sgs = new SparkGenericStreaming(args[0],Integer.parseInt(args[1]));
	JavaPairDStream<String,Integer> wordCounts = sgs.SparkGenericStreamingMain(args);
        wordCounts.foreachRDD(x->{ x.collect().stream().forEach(y->System.out.println(y)); });
        SparkGenericStreaming.ssc.start();
        SparkGenericStreaming.ssc.awaitTermination();
  }
}
