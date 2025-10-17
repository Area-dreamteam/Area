import json
from models.oauth.oauth_login import OAuthLogin
from sqlmodel import SQLModel, select, Session
from sqlalchemy.dialects.postgresql import insert
from models import Service, Action, Reaction
from core.engine import engine
from core.logger import logger


def upsert_data(
    session: Session,
    model,
    values: dict,
    conflict_target,
    update_fields: dict,
    returning_column=None,
):
    stmt = (
        insert(model)
        .values(**values)
        .on_conflict_do_update(
            index_elements=conflict_target
            if isinstance(conflict_target, list)
            else None,
            constraint=conflict_target if isinstance(conflict_target, str) else None,
            set_=update_fields,
        )
    )
    if returning_column is not None:
        stmt = stmt.returning(returning_column)
    return session.exec(stmt)


def sync_reactions_for_service(session: Session, service_data: dict, service_id: int):
    existing_reactions = session.exec(
        select(Reaction).where(Reaction.service_id == service_id)
    ).all()
    existing_reaction_names = {reaction.name for reaction in existing_reactions}

    json_reactions = service_data.get("reactions", [])
    json_reaction_names = {reaction["name"] for reaction in json_reactions}

    reactions_to_delete = existing_reaction_names - json_reaction_names
    if reactions_to_delete:
        for reaction in existing_reactions:
            if reaction.name in reactions_to_delete:
                session.delete(reaction)
                logger.info(
                    f"Deleted reaction: {reaction.name} from service {service_id}"
                )

    for reaction in json_reactions:
        upsert_data(
            session=session,
            model=Reaction,
            values=dict(
                service_id=service_id,
                name=reaction["name"],
                description=reaction.get("description"),
                config_schema=reaction.get("config_schema"),
            ),
            conflict_target="uq_reaction_service_name",
            update_fields=dict(
                description=reaction.get("description"),
                config_schema=reaction.get("config_schema"),
            ),
        )


def sync_actions_for_service(session: Session, service_data: dict, service_id: int):
    existing_actions = session.exec(
        select(Action).where(Action.service_id == service_id)
    ).all()
    existing_action_names = {action.name for action in existing_actions}

    json_actions = service_data.get("actions", [])
    json_action_names = {action["name"] for action in json_actions}

    actions_to_delete = existing_action_names - json_action_names
    if actions_to_delete:
        for action in existing_actions:
            if action.name in actions_to_delete:
                session.delete(action)
                logger.info(f"Deleted action: {action.name} from service {service_id}")

    for action in json_actions:
        upsert_data(
            session=session,
            model=Action,
            values=dict(
                service_id=service_id,
                name=action["name"],
                interval=action["interval"],
                description=action.get("description"),
                config_schema=action.get("config_schema"),
            ),
            conflict_target="uq_action_service_name",
            update_fields=dict(
                description=action.get("description"),
                interval=action["interval"],
                config_schema=action.get("config_schema"),
            ),
        )


def sync_services_oauth_catalog_to_db(session: Session, catalog: dict):
    existing_services = session.exec(select(OAuthLogin)).all()
    existing_service_names = {service.name for service in existing_services}

    json_services = catalog
    json_service_names = set(json_services.keys())

    services_to_delete = existing_service_names - json_service_names
    if services_to_delete:
        for service in existing_services:
            if service.name in services_to_delete:
                session.delete(service)
                logger.info(f"Deleted service: {service.name}")

    for service_data in catalog.values():
        result = upsert_data(
            session=session,
            model=OAuthLogin,
            values=dict(
                name=service_data["name"],
                image_url=service_data.get("image_url"),
                color=service_data.get("color"),
            ),
            conflict_target=["name"],
            update_fields=dict(
                image_url=service_data.get("image_url"),
                color=service_data.get("color"),
            ),
            returning_column=OAuthLogin.id,
        )

    session.commit()
    logger.info("Database synchronization completed")


def sync_services_catalog_to_db(session: Session, catalog: dict):
    existing_services = session.exec(select(Service)).all()
    existing_service_names = {service.name for service in existing_services}

    json_services = catalog
    json_service_names = set(json_services.keys())

    services_to_delete = existing_service_names - json_service_names
    if services_to_delete:
        for service in existing_services:
            if service.name in services_to_delete:
                actions_to_delete = session.exec(
                    select(Action).where(Action.service_id == service.id)
                ).all()
                for action in actions_to_delete:
                    session.delete(action)

                reactions_to_delete = session.exec(
                    select(Reaction).where(Reaction.service_id == service.id)
                ).all()
                for reaction in reactions_to_delete:
                    session.delete(reaction)

                session.delete(service)
                logger.info(
                    f"Deleted service: {service.name} with {len(actions_to_delete)} actions and {len(reactions_to_delete)} reactions"
                )

    for service_data in catalog.values():
        result = upsert_data(
            session=session,
            model=Service,
            values=dict(
                name=service_data["name"],
                description=service_data.get("description"),
                image_url=service_data.get("image_url"),
                color=service_data.get("color"),
                category=service_data.get("category"),
                oauth_required=service_data.get("oauth_required"),
            ),
            conflict_target=["name"],
            update_fields=dict(
                description=service_data.get("description"),
                image_url=service_data.get("image_url"),
                color=service_data.get("color"),
                category=service_data.get("category"),
                oauth_required=service_data.get("oauth_required"),
            ),
            returning_column=Service.id,
        )

        service_id = result.scalar_one()
        sync_actions_for_service(session, service_data, service_id)
        sync_reactions_for_service(session, service_data, service_id)

    session.commit()
    logger.info("Database synchronization completed")


def init_db(catalog: dict, oauths_catalog: dict):
    # print(json.dumps(catalog, indent=2))
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        sync_services_catalog_to_db(session, catalog)
        sync_services_oauth_catalog_to_db(session, oauths_catalog)
