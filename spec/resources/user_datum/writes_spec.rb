require 'rails_helper'

RSpec.describe UserDatumResource, type: :resource do
  describe 'creating' do
    let(:payload) do
      {
        data: {
          type: 'user_data',
          attributes: { }
        }
      }
    end

    let(:instance) do
      UserDatumResource.build(payload)
    end

    it 'works' do
      expect {
        expect(instance.save).to eq(true), instance.errors.full_messages.to_sentence
      }.to change { UserDatum.count }.by(1)
    end
  end

  describe 'updating' do
    let!(:user_datum) { create(:user_datum) }

    let(:payload) do
      {
        data: {
          id: user_datum.id.to_s,
          type: 'user_data',
          attributes: { } # Todo!
        }
      }
    end

    let(:instance) do
      UserDatumResource.find(payload)
    end

    xit 'works (add some attributes and enable this spec)' do
      expect {
        expect(instance.update_attributes).to eq(true)
      }.to change { user_datum.reload.updated_at }
      # .and change { user_datum.foo }.to('bar') <- example
    end
  end

  describe 'destroying' do
    let!(:user_datum) { create(:user_datum) }

    let(:instance) do
      UserDatumResource.find(id: user_datum.id)
    end

    it 'works' do
      expect {
        expect(instance.destroy).to eq(true)
      }.to change { UserDatum.count }.by(-1)
    end
  end
end
