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
import org.apache.spark.api.java.function.VoidFunction2;
import org.apache.spark.api.java.function.VoidFunction;
import org.apache.spark.api.java.function.PairFunction;
import org.apache.spark.api.java.StorageLevels;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaReceiverInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.api.java.StorageLevels;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.Time;

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
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.Encoder;
import org.apache.spark.sql.Encoders;
import org.apache.spark.sql.SparkSession;
import java.util.ArrayList;


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
					System.out.println("JSoup ETL: text:"+text);
					//for (String x : Arrays.asList(SPACE.split(text)))
					//	store(x);
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
			//while(true)
			//{
				try{
					url = new URL(urlargs);
					conn = (HttpURLConnection) url.openConnection();
					conn.setRequestMethod("GET");
					conn.setDoOutput(true);
					br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
					while((input=br.readLine()) != null)
					{
						//System.out.println("Streaming data received:"+input);
						store(input);
					}
				} catch (Exception e) {
					System.out.println("Exception:" + e);
				}
			//}
		}
	}
	else
	{
		Socket s = null;
		BufferedReader br = null;
		String input="";
		try{
			s = new Socket(host,port);
			br = new BufferedReader(new InputStreamReader(s.getInputStream()));
			while(!isStopped() && (input=br.readLine()) != null)
			{
				System.out.println("Streaming data received:"+input);
				store(input);
			}
			s.close();
		} catch (Exception e) {
			System.out.println("Exception:" + e);
		}
	}
  }

  public JavaDStream<String> SparkGenericStreamingMain(String[] args) throws Exception {
    if (args.length > 2) {
     System.err.println("Usage: SparkGenericStreaming <url> (or) SparkGenericStreaming <host> <port>");
     System.exit(1);
    }

    // Create the context with a 5 second batch size
    //SparkConf sparkConf = new SparkConf().setAppName("SparkGenericStreaming");
    sparkConf = new SparkConf().setAppName("SparkGenericStreaming");
    sparkConf.set("spark.driver.allowMultipleContexts","true");
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
    
    //JavaDStream<String> words = lines.flatMap(x->{return Arrays.asList(SPACE.split(x)).iterator();});
    
    //JavaPairDStream<String, Integer> wordCounts = words.mapToPair(
    // new PairFunction<String, String, Integer>() {
    //    @Override
    //    public Tuple2<String, Integer> call(String s) {
    //      return new Tuple2<>(s, 1);
    //    }
    //  }).reduceByKey(new Function2<Integer, Integer, Integer>() {
    //    @Override
    //    public Integer call(Integer i1, Integer i2) {
    //      return i1 + i2;
    //    }
    //  });

    //words.print();
    //wordCounts.print();
    //wordCounts.foreachRDD(x->{ x.collect().stream().forEach(y->System.out.println(y)); });
    //ssc.start();
    //ssc.awaitTermination();
    return words;
  }

  public static void main(String[] args) throws Exception {
	SparkGenericStreaming sgs;
	ArrayList<Word> wordlist = new ArrayList<Word>();
	wordlist.clear();

	if(SparkGenericStreaming.isURLsocket)
		sgs = new SparkGenericStreaming(args[0]);
	else
		sgs = new SparkGenericStreaming(args[0],Integer.parseInt(args[1]));
	JavaDStream<String> words = sgs.SparkGenericStreamingMain(args);

        words.foreachRDD(
		x->{ 
			x.collect().stream().forEach(
				y->{ 
					System.out.println("forEach lambda:"+y);
					Word w = new Word();
					w.setWord(y);
					wordlist.add(w);	
				}
			); 
			SparkSession spark = JavaSparkSingletonInstance.getInstance(x.context().getConf());
			Dataset<Row> wordsdf = spark.createDataFrame(wordlist,Word.class); 
			System.out.println("Saving to Hive Table");
			wordsdf.write().mode("overwrite").saveAsTable("word");
			System.out.println("Saving to Parquet file");
			wordsdf.write().mode("overwrite").parquet("word.parquet");
			wordsdf.printSchema();
			wordlist.clear();
		}
	);


	/*
	words.foreachRDD(new VoidFunction2<JavaRDD<String>, Time>() {
       		@Override
		public void call(JavaRDD<String> rdd, Time time) {
			System.out.println("VoidFunction2.call");
			SparkSession spark = JavaSparkSingletonInstance.getInstance(rdd.context().getConf());
			rdd.foreach(new VoidFunction<String>() {
       				@Override
       				public void call(String word) {
					Word w;
					System.out.println("Function.call");
       					w = new Word();
       					w.setWord(word);
					wordlist.add(w);
       				}
       			});
			Dataset<Row> wordsdf = spark.createDataFrame(wordlist,Word.class); 
			System.out.println("Saving to Hive Table");
			wordsdf.write().mode("overwrite").saveAsTable("word");
			System.out.println("Saving to Parquet file");
			wordsdf.write().mode("overwrite").parquet("word.parquet");
			wordsdf.printSchema();
		}
	});
	*/

	words.print();
        SparkGenericStreaming.ssc.start();
	SparkGenericStreaming.ssc.awaitTermination();
  }
}
