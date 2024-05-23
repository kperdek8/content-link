<?php

/*

Plugin Name: Related Articles Box

Description: Displays a box with links to 5 additional articles on the article page.

Version: 1.0

Author: Sisyphus

*/



// Exit if accessed directly.

if ( ! defined( 'ABSPATH' ) ) {

    exit;

}



// Function to get related articles from an external API

function rab_get_external_related_articles($visitor_id) {

    // Initialize a cURL session

    $ch = curl_init();

    

    // Set the URL for the GET request

    curl_setopt($ch, CURLOPT_URL, "http://flask:5000/get_recommendations/" . urlencode($visitor_id));

    

    // Set the option to return the response as a string

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

    

    // Execute the cURL session

    $response = curl_exec($ch);

    echo $response;

    // Check for cURL errors

    if (curl_errno($ch)) {

        curl_close($ch);

        return [];

    }

    

    // Close the cURL session

    curl_close($ch);

    

    // Decode the JSON response

    $response_data = json_decode($response, true);

    

    // Check if the response data is an array

    if (is_array($response_data)) {

        return $response_data;

    } else {

        return [];

    }

}



// Function to get post URLs from the database

function rab_get_post_urls($post_names) {

    global $wpdb;



    $post_urls = [];



    foreach ($post_names as $post_name) {

        // Prepare and execute the query

        $post_url = $wpdb->get_row(

            $wpdb->prepare(

                "SELECT base, day, month, year FROM post_url WHERE name = %s",

                $post_name

            ),

            ARRAY_A

        );



        if ($post_url) {

            $post_urls[] = trailingslashit($post_url['base']) . "{$post_url['year']}/{$post_url['month']}/{$post_url['day']}/{$post_name}/";

        }

    }



    return $post_urls;

}



// Function to display related articles

function rab_display_related_articles($content) {

    if (is_single() && in_the_loop() && is_main_query()) {

        $visitor_id = '';

        if (isset($_COOKIE['test'])) {

            $visitor_id = base64_decode(sanitize_text_field($_COOKIE['test'])); // Decode and sanitize the visitor ID

        }



        $related_articles = rab_get_external_related_articles($visitor_id);

        $related_urls = rab_get_post_urls($related_articles);



        if (!empty($related_urls)) {

            $content .= '<div class="related-articles-box">';

            $content .= '<h3>Related Articles</h3>';

            $content .= '<ul>';

            foreach ($related_urls as $url) {

                $content .= '<li><a href="' . esc_url($url) . '">' . esc_html($url) . '</a></li>';

            }

            $content .= '</ul>';

            $content .= '</div>';

        }

    }



    return $content;

}

add_filter('the_content', 'rab_display_related_articles');



// Function to enqueue styles

function rab_enqueue_styles() {

    echo '<style>

        .related-articles-box {

            border: 1px solid #ddd;

            padding: 15px;

            margin-top: 20px;

            background-color: #f9f9f9;

        }

        .related-articles-box h3 {

            margin-top: 0;

        }

        .related-articles-box ul {

            list-style-type: none;

            padding-left: 0;

        }

        .related-articles-box ul li {

            margin: 5px 0;

        }

        .related-articles-box ul li a {

            text-decoration: none;

            color: #0073aa;

        }

        .related-articles-box ul li a:hover {

            text-decoration: underline;

        }

    </style>';

}

add_action('wp_head', 'rab_enqueue_styles');

?>