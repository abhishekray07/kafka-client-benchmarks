def print_results(test_name, run_times, num_messages, msg_size):
    print(f"{test_name} Results:")
    print(f"Number of Runs: {len(run_times)}, "
          f"Number of messages: {num_messages}, "
          f"Message Size: {msg_size} bytes.")
    
    total_run_times = sum(run_times)
    time_to_send_messages = total_run_times / len(run_times)
    messages_per_sec = len(run_times) * num_messages / total_run_times
    mb_per_sec = messages_per_sec * msg_size / (1024 * 1024)
    
    print(f"Average Time for {num_messages} messages: {time_to_send_messages} seconds.")
    print(f"Messages / sec: {messages_per_sec}")
    print(f"MB / sec : {mb_per_sec}")