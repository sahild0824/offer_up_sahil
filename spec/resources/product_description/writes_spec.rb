require 'rails_helper'

RSpec.describe ProductDescriptionResource, type: :resource do
  describe 'creating' do
    let(:payload) do
      {
        data: {
          type: 'product_descriptions',
          attributes: { }
        }
      }
    end

    let(:instance) do
      ProductDescriptionResource.build(payload)
    end

    it 'works' do
      expect {
        expect(instance.save).to eq(true), instance.errors.full_messages.to_sentence
      }.to change { ProductDescription.count }.by(1)
    end
  end

  describe 'updating' do
    let!(:product_description) { create(:product_description) }

    let(:payload) do
      {
        data: {
          id: product_description.id.to_s,
          type: 'product_descriptions',
          attributes: { } # Todo!
        }
      }
    end

    let(:instance) do
      ProductDescriptionResource.find(payload)
    end

    xit 'works (add some attributes and enable this spec)' do
      expect {
        expect(instance.update_attributes).to eq(true)
      }.to change { product_description.reload.updated_at }
      # .and change { product_description.foo }.to('bar') <- example
    end
  end

  describe 'destroying' do
    let!(:product_description) { create(:product_description) }

    let(:instance) do
      ProductDescriptionResource.find(id: product_description.id)
    end

    it 'works' do
      expect {
        expect(instance.destroy).to eq(true)
      }.to change { ProductDescription.count }.by(-1)
    end
  end
end
