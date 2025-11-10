"""
Toodledo API Client
Handles all API calls to Toodledo
"""

from typing import Any, Dict, List, Optional

import requests

from config import get_settings
from token_manager import TokenManager


class ToodledoClient:
    """Client for Toodledo API"""

    def __init__(self, token_manager: TokenManager):
        self.settings = get_settings()
        self.token_manager = token_manager
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization"""
        access_token = self.token_manager.get_access_token()
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make HTTP request to Toodledo API"""
        url = f"{self.settings.toodledo_api_base_url}{endpoint}"

        # Toodledo API requires access_token as query parameter
        access_token = self.token_manager.get_access_token()

        if params is None:
            params = {}
        params["access_token"] = access_token

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=30)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        return self._make_request("GET", "/account/get.php")

    def get_tasks(
        self,
        completed: Optional[int] = None,
        before: Optional[int] = None,
        after: Optional[int] = None,
        start: int = 0,
        num: int = 1000,
    ) -> Dict[str, Any]:
        """
        Get tasks from Toodledo

        Args:
            completed: 0=incomplete, 1=completed, -1=all
            before: Get tasks modified before timestamp
            after: Get tasks modified after timestamp
            start: Start position (0-based)
            num: Maximum tasks to return (default 1000, max 1000)

        Returns:
            List of tasks
        """
        params = {"start": start, "num": min(num, 1000)}

        if completed is not None:
            params["comp"] = completed
        if before is not None:
            params["before"] = before
        if after is not None:
            params["after"] = after

        return self._make_request("GET", "/tasks/get.php", params=params)

    def get_folders(self) -> List[Dict[str, Any]]:
        """Get all folders"""
        return self._make_request("GET", "/folders/get.php")

    def get_contexts(self) -> List[Dict[str, Any]]:
        """Get all contexts"""
        return self._make_request("GET", "/contexts/get.php")

    def get_goals(self) -> List[Dict[str, Any]]:
        """Get all goals"""
        return self._make_request("GET", "/goals/get.php")

    def get_locations(self) -> List[Dict[str, Any]]:
        """Get all locations"""
        return self._make_request("GET", "/locations/get.php")

    def create_task(
        self,
        title: str,
        folder: Optional[int] = None,
        context: Optional[int] = None,
        goal: Optional[int] = None,
        location: Optional[int] = None,
        priority: Optional[int] = None,
        duedate: Optional[str] = None,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new task

        Args:
            title: Task title (required)
            folder: Folder ID
            context: Context ID
            goal: Goal ID
            location: Location ID
            priority: -1=negative, 0=low, 1=medium, 2=high, 3=top
            duedate: Due date (YYYY-MM-DD)
            note: Task notes

        Returns:
            Created task data
        """
        task = {"title": title}

        if folder is not None:
            task["folder"] = folder
        if context is not None:
            task["context"] = context
        if goal is not None:
            task["goal"] = goal
        if location is not None:
            task["location"] = location
        if priority is not None:
            task["priority"] = priority
        if duedate is not None:
            task["duedate"] = duedate
        if note is not None:
            task["note"] = note

        data = {"tasks": [task]}
        return self._make_request("POST", "/tasks/add.php", data=data)

    def create_tasks_batch(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple tasks (up to 50)

        Args:
            tasks: List of task dictionaries

        Returns:
            Created tasks data
        """
        if len(tasks) > 50:
            raise ValueError("Cannot create more than 50 tasks at once")

        data = {"tasks": tasks}
        return self._make_request("POST", "/tasks/add.php", data=data)

    def edit_task(self, task_id: int, **kwargs) -> Dict[str, Any]:
        """
        Edit an existing task

        Args:
            task_id: Task ID (required)
            **kwargs: Fields to update

        Returns:
            Updated task data
        """
        task = {"id": task_id}
        task.update(kwargs)

        data = {"tasks": [task]}
        return self._make_request("POST", "/tasks/edit.php", data=data)

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task"""
        data = {"tasks": [task_id]}
        return self._make_request("POST", "/tasks/delete.php", data=data)
