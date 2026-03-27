# Testing
Tests are written to make sure that an application does what it says it will do
and keeps doing so over the course of time.


## Unit testing
- All unit test comprises of a testcase class that inherits `TestCase`, that is
  used to group the test related to a particular model
-

## Testing models

- `setUp()`: This method is called before the execution of every test method inside the TestCase class.
- It implements the code required to set up the test case's environment before the test executes.
- This method can be a good place to set up any local database instance or test variables that may be required for the test cases.

The `setUp` method will be called each time before the execution of any other
method within the testcase

### Check for tearDown() method and what is necessary when running tests in Django


## Testing views
We test views in in Django so you dont have to create an entire application
just to check if the APIs are working. Testing views make it easy to check
endpoints. You can test a view using the ``Client`` module provided by django.
as seen in the ``tests.py`` file.


## Testing models

## Django request factory
why use this in Django and what is the DRF alternative?

## modularizing tests
You can have a sepperats file for each aspect of test like you can have a
`test_models.py` and a `test_views.py` as separate files under a `tests` folder
with `__init__.py` present to tell python that this is a module

page 709 to write the test to the reviews app











