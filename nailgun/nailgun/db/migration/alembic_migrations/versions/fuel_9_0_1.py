#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Fuel 9.0.1

Revision ID: 675105097a69
Revises: 11a9adc6d36a
Create Date: 2016-04-28 22:23:40.895589

"""

from alembic import op
import sqlalchemy as sa

from nailgun.db.sqlalchemy.models import fields

# revision identifiers, used by Alembic.
revision = '675105097a69'
down_revision = '11a9adc6d36a'


def upgrade():
    upgrade_deployment_history()
    upgrade_clusters_replaced_info_wrong_default()
    upgrade_tasks_snapshot()


def downgrade():
    downgrade_tasks_snapshot()
    downgrade_clusters_replaced_info_wrong_default()
    downgrade_deployment_history()


def upgrade_deployment_history():
    op.create_index('deployment_history_task_name_status_idx',
                    'deployment_history',
                    ['deployment_graph_task_name', 'status'])


def downgrade_deployment_history():
    op.drop_index('deployment_history_task_name_status_idx',
                  'deployment_history')


def upgrade_clusters_replaced_info_wrong_default():
    connection = op.get_bind()
    update_query = sa.sql.text(
        "UPDATE clusters SET replaced_deployment_info = '[]' "
        "WHERE replaced_deployment_info = '{}'")
    connection.execute(update_query)


def downgrade_clusters_replaced_info_wrong_default():
    connection = op.get_bind()
    update_query = sa.sql.text(
        "UPDATE clusters SET replaced_deployment_info = '{}' "
        "WHERE replaced_deployment_info = '[]'")
    connection.execute(update_query)


def upgrade_tasks_snapshot():
    op.add_column(
        'tasks',
        sa.Column(
            'tasks_snapshot',
            fields.JSON(),
            nullable=True
        )
    )


def downgrade_tasks_snapshot():
    op.drop_column('tasks', 'tasks_snapshot')
