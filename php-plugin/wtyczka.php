<?php

/*

Plugin Name: ContentLink WP Plugin

Description: Stores user content preferences in MySQL database.

Version: 1.1

Author: Sisyphus

*/



function print_visitor_id_and_url() {

    if (isset($_COOKIE['test'])) {

        global $wpdb; // Access the WordPress database class



        $visitor_id = base64_decode($_COOKIE['test']); // Decode the visitor ID if it is encoded

        echo '<div>ID odwiedzającego: ' . htmlspecialchars($visitor_id) . '</div>'; // Debugging statement

        

        if ($visitor_id === '0') {

            echo '<div style="color: red;">Error: visitor_id is 0. Check if the cookie "test" is set correctly.</div>';

        }



        $full_url = home_url() . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH); // Get full URL and exclude query parameters

        $post_id = get_the_ID(); // Get post ID

        $post_tags = get_the_tags($post_id); // Get post tags



            // Count the number of rows for the current visitor ID

            $row_count = $wpdb->get_var(

                $wpdb->prepare(

                    'SELECT COUNT(*) FROM wp_content_preferences WHERE user_id = %s',

                    $visitor_id

                )

            );



            // Check if the number of rows for visitor is less than 20

            if ($row_count < 20) {

                // Debugging before insert

                echo 'Preparing to insert: User ID = ' . htmlspecialchars($visitor_id) . ', Post URL = ' . htmlspecialchars($full_url) . '<br>';

                

                // Insert new row

                $insert_result = $wpdb->insert(

                    'wp_content_preferences',

                    array(

                        'user_id' => strval($visitor_id), // Force cast to string

                        'post_url' => $full_url

                    ),

                    array('%s', '%s') // Specify data types

                );



                // Check for database errors

                if ($insert_result === false) {

                    echo '<div style="color: red;">Database insert error: ' . $wpdb->last_error . '</div>';

                }



                // Echo the SQL query for debugging

                echo 'SQL Query: ' . htmlspecialchars($wpdb->last_query) . '<br>';



            } else {

                // Update the first row for the current visitor ID

                $update_result = $wpdb->update(

                    'wp_content_preferences',

                    array(

                        'user_id' => strval($visitor_id), // Force cast to string

                        'post_url' => $full_url

                    ),

                    array(

                        'user_id' => $visitor_id

                    ),

                    array('%s', '%s'), // Specify data types

                    array('%s') // Specify where condition data types

                );



                // Check for database errors

                if ($update_result === false) {

                    echo '<div style="color: red;">Database update error: ' . $wpdb->last_error . '</div>';

                }

            }

        

    } else {

        echo '<div style="color: red;">Error: Cookie "test" is not set.</div>';

        wp_enqueue_script('custom_script', plugins_url('set_cookie.js', __FILE__), array(), null, true);

    }

}



// Add print_visitor_id_and_url function to 'wp_footer' hook to execute it every time a footer loads

add_action('wp_footer', 'print_visitor_id_and_url');

?>