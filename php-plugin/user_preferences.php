<?php
/*
Plugin Name: ContentLink User Preferences Plugin
Description: Stores user content preferences in MySQL database.
Version: 2.0
Author: Sisyphus
*/

function print_visitor_id_and_url() {
    if (isset($_COOKIE['content-link'])) {
        global $wpdb; // Access the WordPress database class

        $visitor_id = base64_decode($_COOKIE['content-link']); // Decode the visitor ID if it is encoded
        // echo '<div>ID odwiedzającego: ' . htmlspecialchars($visitor_id) . '</div>'; // Debugging statement
        // if ($visitor_id === '0') {
            // echo '<div style="color: red;">Error: visitor_id is 0. Check if the cookie "content-link" is set correctly.</div>';
        // }

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

	// Check if page URL is related to an article page
	if ($full_url != "http://127.0.0.1:9557/" && strpos($full_url, "http://127.0.0.1:9557/20") == 0) {
		$url_ok = '1';
	} else {
		$url_ok = '0';
	}

        // Check if the number of rows for visitor is less than 20 and exclude home page url insert
        if ($row_count < 20 && $url_ok == '1') {    
            // Insert new row
            $insert_result = $wpdb->insert(
                'wp_content_preferences',
                array(
                    'user_id' => strval($visitor_id), // Force cast to string
                    'post_url' => $full_url
                ),
                array('%s', '%s') // Specify data types
            );

        } elseif ($row_count >= 20 && $url_ok == '1') {
            	// Get the ID of the oldest entry for the current visitor ID
            	$oldest_entry_id = $wpdb->get_var(
            		$wpdb->prepare(
                		'SELECT id FROM wp_content_preferences WHERE user_id = %s ORDER BY edit_date ASC LIMIT 1',
                	   	$visitor_id
                	)
            	);

        	// Update the oldest row for the current visitor ID
        	$update_result = $wpdb->update(
        		'wp_content_preferences',
        	      	array(
        	      		'user_id' => strval($visitor_id), // Force cast to string
        	      		'post_url' => $full_url
        	   	),
        	      	array(
        	      	    	'id' => $oldest_entry_id // Update only the oldest entry
        	      	),
        	       	array('%s', '%s'), // Specify data types
        	    	array('%d') // Specify where condition data types
        	);
       	}
        
    } else {
        wp_enqueue_script('custom_script', plugins_url('set_cookie.js', __FILE__), array(), null, true);
    }
}

// Add print_visitor_id_and_url function to 'wp_footer' hook to execute it every time a footer (page) loads
add_action('wp_footer', 'print_visitor_id_and_url');
?>
