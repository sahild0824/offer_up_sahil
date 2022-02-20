require 'rails_helper'

RSpec.describe "product_descriptions#create", type: :request do
  subject(:make_request) do
    jsonapi_post "/api/v1/product_descriptions", payload
  end

  describe 'basic create' do
    let(:params) do
      {
        # ... your attrs here
      }
    end
    let(:payload) do
      {
        data: {
          type: 'product_descriptions',
          attributes: params
        }
      }
    end

    it 'works' do
      expect(ProductDescriptionResource).to receive(:build).and_call_original
      expect {
        make_request
        expect(response.status).to eq(201), response.body
      }.to change { ProductDescription.count }.by(1)
    end
  end
end
