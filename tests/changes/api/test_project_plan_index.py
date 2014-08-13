from changes.testutils import APITestCase


class ProjectPlanListTest(APITestCase):
    def test_retrieve(self):
        project = self.create_project()
        path = '/api/0/projects/{0}/plans/'.format(
            project.id.hex)

        plan = self.create_plan()
        plan.projects.add(project)

        self.create_plan()

        resp = self.client.get(path)
        assert resp.status_code == 200
        data = self.unserialize(resp)
        assert len(data) == 1
        assert data[0]['id'] == plan.id.hex