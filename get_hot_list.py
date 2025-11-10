#!/usr/bin/env python3
"""
Get Toodledo Hot List - Starred tasks with "Next Action" status
"""

import sys
import requests
from token_manager import TokenManager

def get_hot_list():
    """Retrieve all starred tasks with next action status"""
    try:
        token_manager = TokenManager()
        access_token = token_manager.get_access_token()

        params = {
            'access_token': access_token,
            'comp': 0,  # incomplete tasks only
            'num': 1000,
            'fields': 'star,status,duedate,folder,priority,context'
        }

        response = requests.get('https://api.toodledo.com/3/tasks/get.php', params=params, timeout=10)
        data = response.json()

        # Filter for starred (star=1) and next action (status=1)
        hot_list = [t for t in data[1:] if t.get('star') == 1 and t.get('status') == 1]

        print(f"\n=== Hot List ({len(hot_list)} items) ===\n")
        for i, task in enumerate(hot_list, 1):
            title = task.get('title', 'Untitled')
            due = task.get('duedate', '')
            due_str = f" [Due: {due}]" if due else ""
            print(f"{i}. {title}{due_str}")

        return hot_list

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    get_hot_list()
