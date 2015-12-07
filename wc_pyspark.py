


text_file = spark.textFile("hdfs://MASTER-1:8020/pg25990.txt")
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs://MASTER-1:8020/wc_out")

