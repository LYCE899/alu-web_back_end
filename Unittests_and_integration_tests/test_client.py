#!/usr/bin/env python3
""" Test for client.py """

import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, Mock
import requests
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Test GithubOrgClient """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """ Test org """
        mock_get_json.return_value = {"org": org_name}
        org = GithubOrgClient(org_name)
        self.assertEqual(org.org, mock_get_json.return_value)
        mock_get_json.assert_called_once()

    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        """ Test public repos url """
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/erica/repos"}
        org = GithubOrgClient("erica")
        self.assertEqual(org._public_repos_url, "https://api.github.com/orgs/erica/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """ Test public repos """
        mock_get_json.return_value = [{"name": "testing"}, {"name": "todo-app"}]

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=Mock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/erica/repos"
            org = GithubOrgClient("erica")
            self.assertEqual(org.public_repos(), ["testing", "todo-app"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/erica/repos")
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, has):
        """ Test license """
        has_license = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(has_license, has)

    @parameterized.expand([
        ("google", "apache-2.0", ["repo1"]),
        ("microsoft", "mit", ["repo4"]),
    ])
    @patch("client.get_json")
    def test_public_repos_with_license(self, org_name, license_key, expected_repos, mock_get_json):
        """ Test public repos with license """
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "gpl"}},
            {"name": "repo4", "license": {"key": "mit"}},
        ]

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=Mock) as mock_public_repos_url:
            mock_public_repos_url.return_value = f"https://api.github.com/orgs/{org_name}/repos"
            org = GithubOrgClient(org_name)
            repos = org.public_repos(license=license_key)
            self.assertEqual(repos, expected_repos)
            mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}/repos")
            mock_public_repos_url.assert_called_once()


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Test integration """

    @classmethod
    def setUpClass(cls):
        """ Setup class """
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        options = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """ Tear down class """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test public repos """
        org = GithubOrgClient("test")
        repos = org.public_repos()
        payload = self.repos_payload
        self.assertEqual(repos, self.expected_repos)
        self.assertEqual(payload, self.repos_payload)

    def test_public_repos_with_license(self):
        """ Test public repos with license """
        org = GithubOrgClient("test")
        repos = org.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
