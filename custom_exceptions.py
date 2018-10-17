#!/usr/bin/env python3


class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class LoggedOutError(BaseError):
    def __init__(self):
        super(LoggedOutError, self).__init__("User is currently not logged In")
        # self.message = "User is currently not logged In"


class LoginExpiredError(BaseError):
    def __init__(self):
        super(LoginExpiredError, self).__init__("User's logged has expired")


class LoginRevokedError(BaseError):
    def __init__(self):
        super(LoginRevokedError, self).__init__(
            "User's logged access has been revoked")


class InvalidReviewerPositionError(BaseError):
    def __init__(self):
        message = (
            "The position of the reviewer you provided is not "
            "allowed to review payment voucher at this review stage"
        )
        super(InvalidReviewerPositionError, self).__init__(message)


class DeletedReviewerError(BaseError):
    def __init__(self):
        message = (
            "The reviewer you selected has been deleted so they can't be "
            "selected as a reviewer for any payment vouchers"
        )
        super(DeletedReviewerError, self).__init__(message)


class ReviewerNotFoundError(BaseError):
    def __init__(self):
        message = (
            "The reviewer you selected doesn't exist check and try again"
        )
        super(ReviewerNotFoundError, self).__init__(message)


class InvalidReviewerError(BaseError):
    def __init__(self):
        message = (
            "Reviewer is not authorized to review this payment voucher"
        )
        super(InvalidReviewerError, self).__init__(message)


class EndPaymentReviewProcessError(BaseError):
    def __init__(self):
        message = (
            "Payment voucher has reach the end of the review process. "
            "So you might want to pay or reject the payment"
        )
        super(EndPaymentReviewProcessError, self).__init__(message)


class InvalidVoucherStageError(BaseError):
    def __init__(self, message):
        super(InvalidVoucherStageError, self).__init__(message)


class InvalidPayingOfficer(BaseError):
    def __init__(self):
        super(InvalidPayingOfficer, self).__init__(
            'You are not the authorized cashier for this transaction')
