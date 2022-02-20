class Api::V1::UserMessagingsController < Api::V1::GraphitiController
  def index
    user_messagings = UserMessagingResource.all(params)
    respond_with(user_messagings)
  end

  def show
    user_messaging = UserMessagingResource.find(params)
    respond_with(user_messaging)
  end

  def create
    user_messaging = UserMessagingResource.build(params)

    if user_messaging.save
      render jsonapi: user_messaging, status: 201
    else
      render jsonapi_errors: user_messaging
    end
  end

  def update
    user_messaging = UserMessagingResource.find(params)

    if user_messaging.update_attributes
      render jsonapi: user_messaging
    else
      render jsonapi_errors: user_messaging
    end
  end

  def destroy
    user_messaging = UserMessagingResource.find(params)

    if user_messaging.destroy
      render jsonapi: { meta: {} }, status: 200
    else
      render jsonapi_errors: user_messaging
    end
  end
end
