library(httr)

response_get <- GET("http://127.0.0.1:5000")
print(content(response_get))

response_post <- POST("http://127.0.0.1:5000/compute_gc_content", body = list(file = upload_file('example_1.fastq')))
response_post_content = content(response_post)
print(response_post_content)
