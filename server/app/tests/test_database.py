from unittest.mock import Mock, patch
from sqlmodel import Session

from core.db import (
    upsert_data,
    sync_reactions_for_service,
    sync_actions_for_service,
    sync_services_catalog_to_db,
    sync_services_oauth_catalog_to_db,
    init_db,
)
from models import Service


class TestUpsertData:
    """Test the upsert_data function"""

    def test_upsert_data_with_list_conflict_target(self):
        """Test upsert with list-based conflict target"""
        mock_session = Mock(spec=Session)
        mock_result = Mock()
        mock_session.exec.return_value = mock_result

        values = {"name": "test", "value": "data"}
        conflict_target = ["name"]
        update_fields = {"value": "updated_data"}

        result = upsert_data(
            session=mock_session,
            model=Service,
            values=values,
            conflict_target=conflict_target,
            update_fields=update_fields,
        )

        assert result == mock_result
        mock_session.exec.assert_called_once()

    def test_upsert_data_with_string_conflict_target(self):
        """Test upsert with string-based conflict target"""
        mock_session = Mock(spec=Session)
        mock_result = Mock()
        mock_session.exec.return_value = mock_result

        values = {"name": "test", "value": "data"}
        conflict_target = "unique_constraint"
        update_fields = {"value": "updated_data"}

        result = upsert_data(
            session=mock_session,
            model=Service,
            values=values,
            conflict_target=conflict_target,
            update_fields=update_fields,
        )

        assert result == mock_result
        mock_session.exec.assert_called_once()

    def test_upsert_data_with_returning_column(self):
        """Test upsert with returning column specified"""
        mock_session = Mock(spec=Session)
        mock_result = Mock()
        mock_session.exec.return_value = mock_result

        values = {"name": "test"}
        conflict_target = ["name"]
        update_fields = {"name": "test"}

        result = upsert_data(
            session=mock_session,
            model=Service,
            values=values,
            conflict_target=conflict_target,
            update_fields=update_fields,
            returning_column=Service.id,
        )

        assert result == mock_result
        mock_session.exec.assert_called_once()


class TestSyncReactionsForService:
    """Test sync_reactions_for_service function"""

    def test_sync_reactions_add_new(self):
        """Test adding new reactions"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {
            "reactions": [
                {
                    "name": "new_reaction",
                    "description": "A new reaction",
                    "config_schema": {"type": "object"},
                }
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_reactions_for_service(mock_session, service_data, service_id)

            mock_upsert.assert_called_once()

    def test_sync_reactions_delete_removed(self):
        """Test deleting reactions that are no longer in JSON"""
        mock_existing_reaction = Mock()
        mock_existing_reaction.name = "old_reaction"
        mock_existing_reaction.service_id = 1

        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = [mock_existing_reaction]

        service_data = {"reactions": []}
        service_id = 1

        with patch("core.db.logger") as mock_logger:
            sync_reactions_for_service(mock_session, service_data, service_id)

            mock_session.delete.assert_called_once_with(mock_existing_reaction)
            mock_logger.info.assert_called()

    def test_sync_reactions_update_existing(self):
        """Test updating existing reactions"""
        mock_existing_reaction = Mock()
        mock_existing_reaction.name = "existing_reaction"

        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = [mock_existing_reaction]

        service_data = {
            "reactions": [
                {
                    "name": "existing_reaction",
                    "description": "Updated description",
                    "config_schema": {"type": "updated"},
                }
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_reactions_for_service(mock_session, service_data, service_id)

            mock_upsert.assert_called_once()

    def test_sync_reactions_empty_service_data(self):
        """Test sync with empty service data"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {}
        service_id = 1

        sync_reactions_for_service(mock_session, service_data, service_id)


class TestSyncActionsForService:
    """Test sync_actions_for_service function"""

    def test_sync_actions_add_new(self):
        """Test adding new actions"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {
            "actions": [
                {
                    "name": "new_action",
                    "interval": 60,
                    "description": "A new action",
                    "config_schema": {"type": "object"},
                }
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_actions_for_service(mock_session, service_data, service_id)

            mock_upsert.assert_called_once()

    def test_sync_actions_delete_removed(self):
        """Test deleting actions that are no longer in JSON"""
        mock_existing_action = Mock()
        mock_existing_action.name = "old_action"

        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = [mock_existing_action]

        service_data = {"actions": []}
        service_id = 1

        with patch("core.db.logger") as mock_logger:
            sync_actions_for_service(mock_session, service_data, service_id)

            mock_session.delete.assert_called_once_with(mock_existing_action)
            mock_logger.info.assert_called()

    def test_sync_actions_with_interval_update(self):
        """Test that interval field is properly handled"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {
            "actions": [
                {
                    "name": "timed_action",
                    "interval": 120,
                    "description": "Action with interval",
                }
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_actions_for_service(mock_session, service_data, service_id)

            args, kwargs = mock_upsert.call_args
            assert kwargs["values"]["interval"] == 120
            assert kwargs["update_fields"]["interval"] == 120


class TestSyncServicesCatalogToDB:
    """Test sync_services_catalog_to_db function"""

    def test_sync_services_add_new_service(self):
        """Test adding a new service"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []
        mock_session.commit = Mock()

        mock_result = Mock()
        mock_result.scalar_one.return_value = 1

        catalog = {
            "test_service": {
                "name": "test_service",
                "description": "Test service",
                "category": "test",
                "oauth_required": True,
                "actions": [],
                "reactions": [],
            }
        }

        with (
            patch("core.db.upsert_data", return_value=mock_result) as mock_upsert,
            patch("core.db.sync_actions_for_service") as mock_sync_actions,
            patch("core.db.sync_reactions_for_service") as mock_sync_reactions,
            patch("core.db.logger"),
        ):
            sync_services_catalog_to_db(mock_session, catalog)

            mock_upsert.assert_called_once()
            mock_sync_actions.assert_called_once_with(
                mock_session, catalog["test_service"], 1
            )
            mock_sync_reactions.assert_called_once_with(
                mock_session, catalog["test_service"], 1
            )
            mock_session.commit.assert_called_once()

    def test_sync_services_delete_old_service(self):
        """Test deleting services not in catalog"""
        mock_existing_service = Mock()
        mock_existing_service.name = "old_service"
        mock_existing_service.id = 1

        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.side_effect = [
            [mock_existing_service],
            [],
            [],
        ]
        mock_session.commit = Mock()

        catalog = {}

        with patch("core.db.logger") as mock_logger:
            sync_services_catalog_to_db(mock_session, catalog)

            mock_session.delete.assert_called_with(mock_existing_service)
            mock_logger.info.assert_called()

    def test_sync_services_with_actions_and_reactions(self):
        """Test syncing service with both actions and reactions"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []
        mock_session.commit = Mock()

        mock_result = Mock()
        mock_result.scalar_one.return_value = 1

        catalog = {
            "complex_service": {
                "name": "complex_service",
                "description": "Complex service",
                "actions": [{"name": "action1", "interval": 60}],
                "reactions": [{"name": "reaction1"}],
            }
        }

        with (
            patch("core.db.upsert_data", return_value=mock_result),
            patch("core.db.sync_actions_for_service") as mock_sync_actions,
            patch("core.db.sync_reactions_for_service") as mock_sync_reactions,
            patch("core.db.logger"),
        ):
            sync_services_catalog_to_db(mock_session, catalog)

            mock_sync_actions.assert_called_once()
            mock_sync_reactions.assert_called_once()


class TestSyncServicesOAuthCatalogToDB:
    """Test sync_services_oauth_catalog_to_db function"""

    def test_sync_oauth_services_add_new(self):
        """Test adding new OAuth service"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []
        mock_session.commit = Mock()

        catalog = {
            "github": {"name": "github", "image_url": "github.png", "color": "#000000"}
        }

        with patch("core.db.upsert_data") as mock_upsert, patch("core.db.logger"):
            sync_services_oauth_catalog_to_db(mock_session, catalog)

            mock_upsert.assert_called_once()
            mock_session.commit.assert_called_once()

    def test_sync_oauth_services_delete_old(self):
        """Test deleting OAuth services not in catalog"""
        mock_existing_service = Mock()
        mock_existing_service.name = "old_oauth"

        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = [mock_existing_service]
        mock_session.commit = Mock()

        catalog = {}

        with patch("core.db.logger") as mock_logger:
            sync_services_oauth_catalog_to_db(mock_session, catalog)

            mock_session.delete.assert_called_once_with(mock_existing_service)
            mock_logger.info.assert_called()


class TestInitDB:
    """Test the init_db function"""

    @patch("core.db.Session")
    @patch("core.db.SQLModel")
    @patch("core.db.sync_services_catalog_to_db")
    @patch("core.db.sync_services_oauth_catalog_to_db")
    def test_init_db_success(
        self, mock_sync_oauth, mock_sync_services, mock_sqlmodel, mock_session_class
    ):
        """Test successful database initialization"""
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        catalog = {"service1": {"name": "service1"}}
        oauth_catalog = {"github": {"name": "github"}}

        init_db(catalog, oauth_catalog)

        mock_sqlmodel.metadata.create_all.assert_called_once()
        mock_sync_services.assert_called_once_with(mock_session, catalog)
        mock_sync_oauth.assert_called_once_with(mock_session, oauth_catalog)

    @patch("core.db.Session")
    @patch("core.db.SQLModel")
    @patch("core.db.sync_services_catalog_to_db")
    @patch("core.db.sync_services_oauth_catalog_to_db")
    def test_init_db_with_empty_catalogs(
        self, mock_sync_oauth, mock_sync_services, mock_sqlmodel, mock_session_class
    ):
        """Test database initialization with empty catalogs"""
        mock_session = Mock()
        mock_session_class.return_value.__enter__.return_value = mock_session

        init_db({}, {})

        mock_sync_services.assert_called_once_with(mock_session, {})
        mock_sync_oauth.assert_called_once_with(mock_session, {})


class TestDatabaseEdgeCases:
    """Test edge cases and error conditions"""

    def test_upsert_data_none_values(self):
        """Test upsert with None values"""
        mock_session = Mock(spec=Session)
        mock_result = Mock()
        mock_session.exec.return_value = mock_result

        values = {"name": "test", "description": None}
        conflict_target = ["name"]
        update_fields = {"description": None}

        result = upsert_data(
            session=mock_session,
            model=Service,
            values=values,
            conflict_target=conflict_target,
            update_fields=update_fields,
        )

        assert result == mock_result

    def test_sync_reactions_malformed_data(self):
        """Test sync with malformed reaction data"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {
            "reactions": [
                {"name": "valid_reaction"},
                {"name": "another_valid"},
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_reactions_for_service(mock_session, service_data, service_id)
            assert mock_upsert.call_count == 2

    def test_sync_actions_with_interval(self):
        """Test sync with action that has interval field"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []

        service_data = {
            "actions": [
                {
                    "name": "action_with_interval",
                    "description": "Test action",
                    "interval": 300,
                }
            ]
        }
        service_id = 1

        with patch("core.db.upsert_data") as mock_upsert:
            sync_actions_for_service(mock_session, service_data, service_id)

            args, kwargs = mock_upsert.call_args
            assert kwargs["values"]["interval"] == 300


class TestDatabaseIntegration:
    """Test database operations integration"""

    def test_complete_service_sync_workflow(self):
        """Test complete service synchronization workflow"""
        mock_session = Mock(spec=Session)
        mock_session.exec.return_value.all.return_value = []
        mock_session.commit = Mock()

        mock_result = Mock()
        mock_result.scalar_one.return_value = 1

        catalog = {
            "test_service": {
                "name": "test_service",
                "description": "Complete test service",
                "image_url": "test.png",
                "color": "#ff0000",
                "category": "test",
                "oauth_required": True,
                "actions": [
                    {
                        "name": "test_action",
                        "interval": 300,
                        "description": "Test action",
                        "config_schema": {"type": "object", "properties": {}},
                    }
                ],
                "reactions": [
                    {
                        "name": "test_reaction",
                        "description": "Test reaction",
                        "config_schema": {"type": "object"},
                    }
                ],
            }
        }

        with (
            patch("core.db.upsert_data", return_value=mock_result) as mock_upsert,
            patch("core.db.logger"),
        ):
            sync_services_catalog_to_db(mock_session, catalog)

            assert mock_upsert.call_count == 3
            mock_session.commit.assert_called_once()

