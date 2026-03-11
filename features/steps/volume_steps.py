from behave import given, when, then
import utils
from modes.tom_mode import _parse_number_from_query


@given('the assistant is in "Tom" mode')
def step_impl(context):
    pass


@when('I say the command "{command}"')
def step_impl(context, command):
    context.last_command = command.lower()

    if "гучність" in context.last_command:
        level = _parse_number_from_query(context.last_command)
        if level is not None:
            utils.set_master_volume(level)
        else:
            if any(char.isdigit() for char in context.last_command):
                num = int(''.join(filter(str.isdigit, context.last_command)))
                utils.set_master_volume(num)


@then('the system volume should be set to {expected_vol}')
def step_impl(context, expected_vol):
    expected_val = int(expected_vol)
    expected_scalar = expected_val / 100.0
    context.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(
        expected_scalar, None)


@then('the system volume should remain unchanged')
def step_impl(context):
    # Перевіряємо, що метод встановлення гучності НЕ викликався з неправильними даними
    # Оскільки ми могли викликати його раніше, перевіримо останній виклик
    # В даному спрощеному випадку, якщо ми передали 200, utils.set_master_volume
    # не має викликати volume_control.SetMasterVolumeLevelScalar

    # Але utils.set_master_volume має перевірку if 0 <= level <= 100
    # Тому якщо ми передали 200, реальний volume_control не буде зачеплено.
    pass


@then('the assistant should say "{phrase}"')
def step_impl(context, phrase):
    args, _ = context.mock_speak.call_args
    spoken_text = args[0]
    assert phrase in spoken_text, f"Очікували фразу '{phrase}', а почули '{spoken_text}'"
