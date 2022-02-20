class Api::V1::UserDataController < Api::V1::GraphitiController
  def index
    user_data = UserDatumResource.all(params)
    respond_with(user_data)
  end

  def show
    user_datum = UserDatumResource.find(params)
    respond_with(user_datum)
  end

  def create
    user_datum = UserDatumResource.build(params)

    if user_datum.save
      render jsonapi: user_datum, status: :created
    else
      render jsonapi_errors: user_datum
    end
  end

  def update
    user_datum = UserDatumResource.find(params)

    if user_datum.update_attributes
      render jsonapi: user_datum
    else
      render jsonapi_errors: user_datum
    end
  end

  def destroy
    user_datum = UserDatumResource.find(params)

    if user_datum.destroy
      render jsonapi: { meta: {} }, status: :ok
    else
      render jsonapi_errors: user_datum
    end
  end
end
