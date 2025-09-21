# GitHub Agent Client Documentation

## Overview

The GitHub Agent Client is a simple, V2-compliant tool that allows agents to access GitHub repositories and data through the GitHub API. It provides authentication, repository management, and basic GitHub operations.

## Features

- ✅ **Authentication**: Secure token-based authentication
- ✅ **Repository Access**: List, search, and retrieve repository information
- ✅ **File Operations**: Read repository contents and file data
- ✅ **User Information**: Get user profiles and statistics
- ✅ **Rate Limiting**: Monitor API rate limits
- ✅ **Error Handling**: Comprehensive error handling and reporting
- ✅ **V2 Compliance**: Under 400 lines, simple design, no complex patterns

## Installation & Setup

### Prerequisites

- Python 3.7+
- `requests` library
- GitHub personal access token

### Configuration

The client uses a JSON configuration file with the following structure:

```json
{
  "username": "your_github_username",
  "token": "ghp_your_personal_access_token",
  "setup_date": "2025-01-17T19:00:00Z",
  "wizard_version": "1.0"
}
```

**Default Configuration Locations:**
1. `D:/projectscanner/config/github_config.json` (Primary)
2. `config/github_config.json` (Secondary)
3. `github_config.json` (Fallback)

## Usage

### Command Line Interface

```bash
# Test connection
python github_agent_client_standalone.py --test --config path/to/config.json

# Get repositories for a user
python github_agent_client_standalone.py --repos username --config path/to/config.json

# Get user information
python github_agent_client_standalone.py --user username --config path/to/config.json

# Search repositories
python github_agent_client_standalone.py --search "python machine learning" --config path/to/config.json

# Check rate limit
python github_agent_client_standalone.py --rate-limit --config path/to/config.json
```

### Python API

```python
from github_agent_client_standalone import GitHubAgentClient

# Initialize client
client = GitHubAgentClient('path/to/config.json')

# Test connection
result = client.test_connection()
print(f"Status: {result['status']}")
print(f"Username: {result['username']}")

# Get repositories
repos = client.get_repositories('username', per_page=10)
for repo in repos:
    print(f"{repo.full_name} - {repo.stars} stars")

# Get repository information
repo_info = client.get_repository_info('owner', 'repo-name')

# Get file content
content = client.get_file_content('owner', 'repo-name', 'path/to/file.py')

# Search repositories
search_results = client.search_repositories('python web framework')

# Get user information
user_info = client.get_user_info('username')

# Check rate limit
rate_limit = client.get_rate_limit()
print(f"Remaining: {rate_limit['rate']['remaining']}")
```

## API Reference

### GitHubAgentClient

#### Constructor
```python
GitHubAgentClient(config_path: str = None)
```
- `config_path`: Path to GitHub configuration file (optional)

#### Methods

##### `test_connection() -> Dict[str, Any]`
Test GitHub API connection and authentication.

**Returns:**
```python
{
    "status": "success|error",
    "authenticated": bool,
    "username": str,
    "name": str,
    "email": str,
    "public_repos": int,
    "private_repos": int
}
```

##### `get_repositories(username: str = None, per_page: int = 30) -> List[GitHubRepository]`
Get repositories for a user.

**Parameters:**
- `username`: GitHub username (defaults to config username)
- `per_page`: Number of repositories to retrieve (max 100)

**Returns:** List of `GitHubRepository` objects

##### `get_repository_info(owner: str, repo: str) -> Dict[str, Any]`
Get detailed information about a specific repository.

**Parameters:**
- `owner`: Repository owner username
- `repo`: Repository name

**Returns:** Dictionary with repository details

##### `get_repository_contents(owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]`
Get contents of a repository directory.

**Parameters:**
- `owner`: Repository owner username
- `repo`: Repository name
- `path`: Directory path (empty for root)

**Returns:** List of file/directory objects

##### `get_file_content(owner: str, repo: str, path: str) -> str`
Get content of a specific file.

**Parameters:**
- `owner`: Repository owner username
- `repo`: Repository name
- `path`: File path

**Returns:** File content as string

##### `search_repositories(query: str, per_page: int = 30) -> List[GitHubRepository]`
Search for repositories.

**Parameters:**
- `query`: Search query string
- `per_page`: Number of results to retrieve (max 100)

**Returns:** List of `GitHubRepository` objects

##### `get_user_info(username: str = None) -> Dict[str, Any]`
Get user information.

**Parameters:**
- `username`: GitHub username (defaults to config username)

**Returns:** Dictionary with user details

##### `get_rate_limit() -> Dict[str, Any]`
Get API rate limit information.

**Returns:**
```python
{
    "rate": {
        "limit": int,
        "remaining": int,
        "reset": int
    }
}
```

### Data Models

#### GitHubRepository
```python
@dataclass
class GitHubRepository:
    name: str                    # Repository name
    full_name: str              # Full repository name (owner/repo)
    description: Optional[str]  # Repository description
    url: str                    # GitHub URL
    clone_url: str              # Git clone URL
    language: Optional[str]     # Primary programming language
    stars: int                  # Number of stars
    forks: int                  # Number of forks
    size: int                   # Repository size in KB
    updated_at: str             # Last update timestamp
    private: bool               # Whether repository is private
```

#### GitHubConfig
```python
@dataclass
class GitHubConfig:
    username: str      # GitHub username
    token: str         # Personal access token
    setup_date: str    # Configuration setup date
    wizard_version: str # Configuration wizard version
```

## Error Handling

The client provides comprehensive error handling:

- **Authentication Errors**: Invalid or expired tokens
- **Rate Limiting**: API rate limit exceeded
- **Network Errors**: Connection timeouts and network issues
- **API Errors**: GitHub API errors (404, 403, etc.)
- **File Errors**: Missing configuration files

All errors are wrapped in descriptive exception messages with context.

## Rate Limiting

GitHub API has rate limits:
- **Authenticated requests**: 5,000 requests per hour
- **Unauthenticated requests**: 60 requests per hour

The client includes rate limit monitoring and will throw exceptions when limits are exceeded.

## Security Considerations

- **Token Security**: Store tokens securely, never commit to version control
- **Environment Variables**: Consider using environment variables for production
- **Access Permissions**: Use minimal required permissions for tokens
- **HTTPS Only**: All API calls use HTTPS encryption

## Examples

### Basic Repository Operations

```python
from github_agent_client_standalone import GitHubAgentClient

client = GitHubAgentClient()

# List user repositories
repos = client.get_repositories('octocat')
for repo in repos[:5]:
    print(f"{repo.full_name}: {repo.description}")

# Get specific repository
repo_info = client.get_repository_info('octocat', 'Hello-World')
print(f"Stars: {repo_info['stargazers_count']}")

# Read a file
content = client.get_file_content('octocat', 'Hello-World', 'README')
print(content)
```

### Search and Discovery

```python
# Search for Python repositories
python_repos = client.search_repositories('language:python stars:>1000')
for repo in python_repos[:10]:
    print(f"{repo.full_name} - {repo.stars} stars")

# Get user information
user_info = client.get_user_info('octocat')
print(f"User: {user_info['name']}")
print(f"Followers: {user_info['followers']}")
```

### Rate Limit Monitoring

```python
# Check rate limit before making requests
rate_limit = client.get_rate_limit()
remaining = rate_limit['rate']['remaining']

if remaining < 100:
    print("Warning: Low rate limit remaining")
else:
    # Make API calls
    repos = client.get_repositories()
```

## Troubleshooting

### Common Issues

1. **"GitHub configuration file not found"**
   - Ensure config file exists in one of the default locations
   - Check file path and permissions

2. **"HTTP 401: Unauthorized"**
   - Verify token is valid and not expired
   - Check token permissions

3. **"HTTP 403: Forbidden"**
   - Rate limit exceeded
   - Insufficient token permissions

4. **"HTTP 404: Not Found"**
   - Repository or user doesn't exist
   - Check spelling and case sensitivity

### Debug Mode

Enable debug output by setting environment variable:
```bash
export GITHUB_DEBUG=1
python github_agent_client_standalone.py --test
```

## Contributing

When contributing to the GitHub Agent Client:

1. **V2 Compliance**: Keep files under 400 lines
2. **Simple Design**: Avoid complex patterns and inheritance
3. **Error Handling**: Provide clear error messages
4. **Testing**: Add tests for new functionality
5. **Documentation**: Update this documentation

## License

This tool is part of the Agent Cellphone V2 project and follows the same licensing terms.

---

**Last Updated:** 2025-01-17  
**Version:** 1.0  
**Maintainer:** Agent-2 (Architecture & Design Specialist)


