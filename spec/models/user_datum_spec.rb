require 'rails_helper'

RSpec.describe UserDatum, type: :model do
  
    describe "Direct Associations" do

    it { should have_many(:user_messagings) }

    it { should have_many(:seller_id) }

    end

    describe "InDirect Associations" do

    end

    describe "Validations" do

    end
end
