print('\nRead next article before start:')
print('https://www.ibm.com/developerworks/library/os-pythondescriptors/index.html')


class DataDescriptor:
    def _print_current_x(self):
        print(f'  current value: {self._x}')

    def __init__(self, initial_value=None):
        print('DataDescriptor.__init__() call')
        self._x = initial_value or 'Initial value'
        self._print_current_x()

    def __get__(self, instance, owner):
        print('DataDescriptor.__get__() call')
        print(f'  instance = {instance}')  # Debug
        print(f'  owner = {owner}')  # Debug
        self._print_current_x()
        return self._x

    def __set__(self, instance, value):
        print('DataDescriptor.__set__() call')
        self._x = value
        self._print_current_x()

    def __delete__(self, instance):
        print('DataDescriptor.__delete__() call')
        self._x = 'Deleted value.'
        self._print_current_x()


class DescriptorHolder:
    print('\nInitialize descriptor')
    data_descriptor = DataDescriptor()  # DataDescriptor.__init__() call


# Make instance
descriptor_holder = DescriptorHolder()

##
# Let's start to play!
##

print('\nCheck __get__ from instance')
descriptor_holder.data_descriptor  # DataDescriptor.__get__() call

print('\nCheck __set__ from instance')
descriptor_holder.data_descriptor = 'New value'  # DataDescriptor.__set__() call

print('\nCheck __delete__ from instance')
del descriptor_holder.data_descriptor  # DataDescriptor.__delete__() call

print('\nReinitialize')
DescriptorHolder.data_descriptor = DataDescriptor()  # DataDescriptor.__init__() call

print('\nCheck __get__ from class')
DescriptorHolder.data_descriptor  # DataDescriptor.__get__() call

print('\nCheck __set__ from class')
DescriptorHolder.data_descriptor = 'Replaced string'
# Whoops! Our descriptor was replaced with a string!!
print(f"Currently DescriptorHolder.data_descriptor = '{DescriptorHolder.data_descriptor}'")

print('\nReinitialize')
DescriptorHolder.data_descriptor = DataDescriptor()  # DataDescriptor.__init__() call

print('\nCheck __delete__ from class')
del DescriptorHolder.data_descriptor
# Oh... No... We have lost our descriptor once again...
# And have deleted it from __dict__...
print("'data_descriptor' in DescriptorHolder.__dict__?",
      'data_descriptor' in DescriptorHolder.__dict__)  # False

print("""
Conclusion:
Never use classes to set and delete descriptor values!

Task: 
1. Comment out __set__ or __delete__ method in the DataDescriptor and run this code again.
2. Comment our both, __set__ and __delete__ methods in the DataDescriptor and run this code again.""")

print('\nLet\'s set both, class attribute and instance attribute.')
descriptor_holder.data_descriptor = DataDescriptor('2')
DescriptorHolder.data_descriptor = DataDescriptor('1')
descriptor_holder.data_descriptor  # 1
# If the descriptor is in the class - the instance descriptor will be ignored
# The way to access the instance descriptor is to get it from __dict__
descriptor_holder.__dict__['data_descriptor'].__get__(descriptor_holder, DescriptorHolder)
# If you delete the descriptor from class you will still not have access to the descriptor of the instance
# See below why...

print('\nReinitialize')
DescriptorHolder.data_descriptor = DataDescriptor()  # DataDescriptor.__init__() call

del DescriptorHolder.data_descriptor  # can delete!
print("'data_descriptor' in DescriptorHolder.__dict__?",
      'data_descriptor' in DescriptorHolder.__dict__)  # False

print('\nAssign descriptor to the instance')
# OK, now we have no descriptors, let's assign one to the instance.
descriptor_holder.data_descriptor = DataDescriptor()
descriptor_holder.data_descriptor  # no effect!
descriptor_holder.data_descriptor = 'Fail'  # descriptor has been replaced!
print(descriptor_holder.data_descriptor)  # prints 'Fail'
print('\nAssign once again and try to delete')
descriptor_holder.data_descriptor = DataDescriptor()
del descriptor_holder.data_descriptor  # you can delete it!
print("'data_descriptor' in descriptor_holder.__dict__?",
      'data_descriptor' in descriptor_holder.__dict__)  # False

print("""
Conclusion:
You can assign descriptor to the class instance, but it makes no effect.
You see that the descriptors work properly only inside classes.
Inside instances it acts as regular variable that you can assign or delete.""")


print('\nImplement non data descriptor')
class NonDataDescriptor:
    def _print_current_x(self):
        print(f'  current value: {self._x}')

    def __init__(self, initial_value=None):
        print('NonDataDescriptor.__init__() call')
        self._x = initial_value or 'Initial value'
        self._print_current_x()

    def __get__(self, instance, owner):
        print('NonDataDescriptor.__get__() call')
        print(f'  instance = {instance}')  # Debug
        print(f'  owner = {owner}')  # Debug
        self._print_current_x()
        return self._x

    # def __set__(self, instance, value):
    #     pass

    def __delete__(self, instance):
        print('NonDataDescriptor.__delete__() call')
        self._x = 'Deleted value.'
        self._print_current_x()


print('\nClass has NonDataDescriptor, instance has DataDescriptor')
DescriptorHolder.data_descriptor = NonDataDescriptor()
descriptor_holder.__dict__['data_descriptor'] = DataDescriptor()
DescriptorHolder.data_descriptor
descriptor_holder.data_descriptor
print('Class descriptor is used.')

print('\nClass has DataDescriptor, instance has NonDataDescriptor')
DescriptorHolder.data_descriptor = DataDescriptor()
descriptor_holder.__dict__['data_descriptor'] = NonDataDescriptor()
DescriptorHolder.data_descriptor
descriptor_holder.data_descriptor
print('Class descriptor is used.')  # As expected.
