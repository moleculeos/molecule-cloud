from django.test import TestCase
from file_storage.models import Directory, File
from django.contrib.auth.models import User


class FileAndDirTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='testuser1', email='test1@test.com', password='testpassword')
        self.share_user = User.objects.create(username='testuser2', email='test2@test.com', password='testpassword')

        self.root = Directory.objects.create(
            root=True,
            name='root',
            parent=None,
            owner=User.objects.all()[0],
        )

        self.dir1 = Directory.objects.create(
            root=False,
            name='1',
            parent=self.root,
            owner=self.test_user,
        )

        self.test_file = File.objects.create(
            directory=self.dir1,
            name='test_file',
            owner=self.test_user,
            filetype='test',
        )




class ShareRootDirTestCase(FileAndDirTestCase):
    def setUp(self):
        super().setUp()
        self.root.shared_to.add(self.share_user)

    def test_is_share_root_work(self):
        self.assertEqual(self.root.public_to.first(), self.share_user)

    def test_is_child_dir_shared(self):
        self.assertEqual(self.dir1.public_to.first(), self.share_user)

    def test_is_file_in_child_dir_shared(self):
        self.assertEqual(self.test_file.public_to.first(), self.share_user)


class ShareDirTestCase(FileAndDirTestCase):
    def setUp(self):
        super().setUp()
        self.dir1.shared_to.add(self.share_user)

    def test_is_share_dir_work(self):
        self.assertEqual(self.dir1.public_to.first(), self.share_user)

    def test_is_file_in_dir_shared(self):
        self.assertEqual(self.test_file.public_to.first(), self.share_user)


class ShareFileTestCase(FileAndDirTestCase):
    def setUp(self):
        super().setUp()
        self.test_file.shared_to.add(self.share_user)

    def test_share_file(self):
        self.assertEqual(self.test_file.public_to.first(), self.share_user)