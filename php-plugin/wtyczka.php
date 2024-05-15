<?php
/*
Plugin Name: ContentLink WP Plugin
Description: Stores user content preferences in MySQL database.
Version: 1.0
Author: Sisyphus
*/

function print_visitor_id_and_url() {
    if (isset($_COOKIE['test'])) {
        global $wpdb; // Access the WordPress database class

        $visitor_id = strval($_COOKIE['test']); // Get visitor ID from cookies
        echo '<div>ID odwiedzającego: ' . $visitor_id . '</div>';
        $full_url = home_url() . $_SERVER['REQUEST_URI']; // Get full url
        $post_id = get_the_ID(); // Get post ID
        $post_tags = get_the_tags($post_id); // Get post tags

        // Check if a row with the given user_id and post_url already exists
        $existing_row = $wpdb->get_row(
            $wpdb->prepare(
                'SELECT * FROM wp_content_preferences WHERE user_id = %s AND post_url = %s',
                $visitor_id,
                $full_url
            )
        );

        if(!$existing_row) {
            // Count the number of rows for the current visitor ID
            $row_count = $wpdb->get_var(
                $wpdb->prepare(
                    'SELECT COUNT(*) FROM wp_content_preferences WHERE user_id = %s',
                    $visitor_id
                )
            );

            // Check if the number of rows for visitor is less than 20
            if ($row_count < 20) {
                // Insert new row
                $wpdb->insert(
                    'wp_content_preferences',
                    array(
                        'user_id' => $visitor_id,
                        'post_url' => $full_url
                    )
                );

                // Echo the SQL query for debugging
                echo 'SQL Query: ' . $wpdb->last_query . '<br>';

            } else {
                // Update the first row for the current visitor ID
                $wpdb->update(
                    'wp_content_preferences',
                    array(
                        'user_id' => $visitor_id,
                        'post_url' => $full_url
                    ),
                    array(
                        'user_id' => $visitor_id
                    )
                );
            }
        }
        
        // Print visitor ID and full url in the footer
        // echo '<div>ID odwiedzającego: ' . $visitor_id . '</div>';
        // echo '<div>Aktualny URL: ' . $full_url . '</div>';
        // if ($post_tags) {
            // echo '<div>Tagi postu:';
            // foreach ($post_tags as $tag) {
                // echo ' ' . $tag->name . ',';
            // }
            // echo '</div>';
        // } else {
            // echo '<div>Brak tagów</div>';
        // }

    } else {
        wp_enqueue_script('custom_script', plugins_url('set_cookie.js', __FILE__), array(), null, true);
    }
}

// Add prtin_visitor_id_and_url function to 'wp_footer' hook to execute it every time a footer loads
add_action('wp_footer', 'print_visitor_id_and_url');
?>