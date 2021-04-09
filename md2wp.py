import sys
import os
import time
import datetime
import re
import markdown
import html
from slugify import slugify

root_path         = "d:\\temp\\blog"                            # Path to read markdown files from
blog_title        = "Jonathan Wrote This"                       # Title of Blog (only needed for data integrity)
subdomain         = "jonathanwrotethis"                         # Wordpress subdomain (only needed for data integrity)
author_name       = "Jonathan"                                  # Name to give author of each post (only needed for data integrity)
author_first_name = "Jonathan"                                  # First name of author (only needed for data integrity)
author_last_name  = "Beckett"                                   # Last name of author (only needed for data integrity)
author_email      = "jonathan.beckett@gmail.com"                # Email address of author (only needed for data integrity)
blog_url          = "https://jonathanwrotethis.wordpress.com"   # URL of blog (only needed for data integrity)
today_date        = "2021-04-09T00:00:00Z"                      # Today's date
post_category     = "Life"                                      # Default category for each post
output_filename   = "d:\\temp\\wp.xml"                          # Output filename

# Start the XML
xml = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
    "<rss version=\"2.0\" xmlns:excerpt=\"http://wordpress.org/export/1.2/excerpt/\" xmlns:content=\"http://purl.org/rss/1.0/modules/content/\" xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:wp=\"http://wordpress.org/export/1.2/\" >\n"
    "<channel>\n"
    "<title>" + blog_title + "</title>\n"
    "<link>" + blog_url + "</link>\n"
    "<description></description>\n"
    "<pubDate>Sun, 04 Apr 2021 12:08:52 +0000</pubDate>\n"
    "<language></language>\n"
    "<wp:wxr_version>1.2</wp:wxr_version>\n"
    "<wp:base_site_url>http://wordpress.com/</wp:base_site_url>\n"
    "<wp:base_blog_url>" + blog_url + "</wp:base_blog_url>\n"
    "<wp:author>\n"
    "<wp:author_id>12345678</wp:author_id>"
    "<wp:author_login><![CDATA[" + subdomain + "]]></wp:author_login>"
    "<wp:author_email><![CDATA[" + author_email + "]]></wp:author_email>"
    "<wp:author_display_name><![CDATA[" + author_name + "]]></wp:author_display_name>"
    "<wp:author_first_name><![CDATA[" + author_first_name + "]]></wp:author_first_name>"
    "<wp:author_last_name><![CDATA[" + author_last_name + "]]></wp:author_last_name>"
	"</wp:author>")


i=123456

for subdir, dirs, files in os.walk(root_path):
    for file in files:
        if '.txt' in file and '2019' not in file and '2020' not in file and '2021' not in file and 'readme' not in file:
            
            print("Processing " + file)
            
            i = i + 1
            
            # Read the file contents
            markdown_file_full_path = os.path.join(subdir, file)
            markdown_file = open(markdown_file_full_path,'r')
            markdown_text = markdown_file.read()
            
            # split the line into files, and chop the top 4 off
            # (to get rid of the title and date, as output by wp2md)
            markdown_text_lines = markdown_text.splitlines()
            hybrid_text_lines = []
            hybrid_text_lines += markdown_text_lines[4:]
            
            # build the post title and body
            
            # Title
            post_title              = markdown_text_lines[0].replace('# ','')
            post_title_html_escaped = html.escape(post_title)
            
            # Body
            post_body              = '\r\n'.join(hybrid_text_lines)
            post_body_html         = markdown.markdown(html.escape(post_body))
            # post_body_html_escaped = html.escape(post_body_html)
            
            # Extract the date from the filename
            # (so we may use it to back-date the post into write.as)
            year      = file[0:4]
            month     = file[5:7]
            day       = file[8:10]
            post_date = year + '-' + month + '-' + day + ' 00:00:00';
            
            # generate a publish date in the appropriate format - e.g. Mon, 20 Jan 2020 00:00:00 +0000
            pubdate = datetime.datetime(int(year), int(month), int(day))
            
            pubdate_formatted = pubdate.strftime("%a %d %b %Y %H:%M:%S")
            
            slug = slugify(post_title)
            
            xml = xml + "<item>\n"
            xml = xml + "  <title>" + post_title + "</title>\n"
            xml = xml + "  <link>" + blog_url + "/" + year + "/" + month + "/" + day + "/" + slug + "/</link>\n"
            xml = xml + "  <pubDate>" + pubdate_formatted + "</pubDate>\n"
            xml = xml + "  <dc:creator>" + subdomain + "</dc:creator>\n"
            xml = xml + "  <guid isPermaLink=\"false\">" + blog_url + "/" + year + "/" + month + "/" + day + "/" + slug + ".html</guid>\n"
            xml = xml + "  <description></description>\n"
            xml = xml + "  <content:encoded><![CDATA[" + post_body_html + "]]></content:encoded>\n"
            xml = xml + "  <excerpt:encoded><![CDATA[]]></excerpt:encoded>\n"
            xml = xml + "  <wp:post_id>" + str(i) + "</wp:post_id>\n"
            xml = xml + "  <wp:post_date>" + post_date + "</wp:post_date>\n"
            xml = xml + "  <wp:post_date_gmt>" + post_date + "</wp:post_date_gmt>\n"
            xml = xml + "  <wp:comment_status>open</wp:comment_status>\n"
            xml = xml + "  <wp:ping_status>open</wp:ping_status>\n"
            xml = xml + "  <wp:post_name>" + slug + "</wp:post_name>\n"
            xml = xml + "  <wp:status>publish</wp:status>\n"
            xml = xml + "  <wp:post_parent>0</wp:post_parent>\n"
            xml = xml + "  <wp:menu_order>0</wp:menu_order>\n"
            xml = xml + "  <wp:post_type>post</wp:post_type>\n"
            xml = xml + "  <wp:post_password></wp:post_password>\n"
            xml = xml + "  <wp:is_sticky>0</wp:is_sticky>\n"
            xml = xml + "  <category domain=\"category\" nicename=\"life\"><![CDATA[Life]]></category>\n"
            xml = xml + "</item>\n"

# End the XML
xml = xml + "</channel>\n</rss>\n"

# Output the XML to a file
post_file = open(output_filename, "w")
post_file.write(xml)
post_file.close()
