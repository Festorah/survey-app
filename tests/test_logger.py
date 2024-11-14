import logging

from src.logger import setup_logging


def test_setup_logging(mocker):
    # Mock `basicConfig` and `getLogger`
    mock_basic_config = mocker.patch("logging.basicConfig")
    mock_get_logger = mocker.patch("logging.getLogger")

    # Mock the handlers
    mock_file_handler = mocker.Mock(spec=logging.FileHandler)
    mock_file_handler.baseFilename = "app.log"
    mock_stream_handler = mocker.Mock(spec=logging.StreamHandler)

    # Patch `FileHandler` and `StreamHandler` to return these mocks
    mocker.patch("logging.FileHandler", return_value=mock_file_handler)
    mocker.patch("logging.StreamHandler", return_value=mock_stream_handler)

    # Call the setup_logging function
    logger = setup_logging()

    mock_basic_config.assert_called_once()
    config_args = mock_basic_config.call_args.kwargs

    assert config_args["level"] == logging.INFO
    assert (
        config_args["format"] == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Check handlers
    handlers = config_args["handlers"]
    assert len(handlers) == 2
    assert mock_file_handler in handlers
    assert mock_stream_handler in handlers
    mock_get_logger.assert_called_once_with("SurveyApp")

    # Verify that the returned logger is the mock_logger instance
    mock_logger = mock_get_logger.return_value
    assert logger == mock_logger
