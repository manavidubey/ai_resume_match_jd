import React, { useState } from 'react';

interface JobDescriptionFormProps {
  onSubmit: (jobData: any) => void;
}

const JobDescriptionForm: React.FC<JobDescriptionFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_skills: [] as string[],
    preferred_skills: [] as string[],
    experience_required: '',
    role_responsibilities: [] as string[]
  });
  
  const [newSkill, setNewSkill] = useState('');
  const [newResponsibility, setNewResponsibility] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const addRequiredSkill = () => {
    if (newSkill.trim() && !formData.required_skills.includes(newSkill.trim())) {
      setFormData(prev => ({
        ...prev,
        required_skills: [...prev.required_skills, newSkill.trim()]
      }));
      setNewSkill('');
    }
  };

  const removeRequiredSkill = (index: number) => {
    setFormData(prev => ({
      ...prev,
      required_skills: prev.required_skills.filter((_, i) => i !== index)
    }));
  };

  const addPreferredSkill = () => {
    if (newSkill.trim() && !formData.preferred_skills.includes(newSkill.trim())) {
      setFormData(prev => ({
        ...prev,
        preferred_skills: [...prev.preferred_skills, newSkill.trim()]
      }));
      setNewSkill('');
    }
  };

  const removePreferredSkill = (index: number) => {
    setFormData(prev => ({
      ...prev,
      preferred_skills: prev.preferred_skills.filter((_, i) => i !== index)
    }));
  };

  const addResponsibility = () => {
    if (newResponsibility.trim() && !formData.role_responsibilities.includes(newResponsibility.trim())) {
      setFormData(prev => ({
        ...prev,
        role_responsibilities: [...prev.role_responsibilities, newResponsibility.trim()]
      }));
      setNewResponsibility('');
    }
  };

  const removeResponsibility = (index: number) => {
    setFormData(prev => ({
      ...prev,
      role_responsibilities: prev.role_responsibilities.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
        <div className="sm:col-span-4">
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Job Title
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="title"
              id="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        </div>

        <div className="sm:col-span-6">
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Job Description
          </label>
          <div className="mt-1">
            <textarea
              id="description"
              name="description"
              rows={6}
              value={formData.description}
              onChange={handleChange}
              required
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        </div>

        <div className="sm:col-span-6">
          <label className="block text-sm font-medium text-gray-700">
            Required Skills
          </label>
          <div className="mt-1 flex">
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              placeholder="Add a required skill"
              className="flex-1 rounded-l-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            <button
              type="button"
              onClick={addRequiredSkill}
              className="inline-flex items-center rounded-r-md border border-l-0 border-gray-300 bg-gray-50 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Add
            </button>
          </div>
          <div className="mt-2">
            {formData.required_skills.map((skill, index) => (
              <span key={index} className="inline-flex items-center rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-800 mr-2 mb-2">
                {skill}
                <button
                  type="button"
                  onClick={() => removeRequiredSkill(index)}
                  className="ml-2 flex-shrink-0 rounded-full bg-indigo-100 text-indigo-500 hover:bg-indigo-200 focus:outline-none"
                >
                  <span className="sr-only">Remove</span>
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div className="sm:col-span-6">
          <label className="block text-sm font-medium text-gray-700">
            Preferred Skills
          </label>
          <div className="mt-1 flex">
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              placeholder="Add a preferred skill"
              className="flex-1 rounded-l-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            <button
              type="button"
              onClick={addPreferredSkill}
              className="inline-flex items-center rounded-r-md border border-l-0 border-gray-300 bg-gray-50 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Add
            </button>
          </div>
          <div className="mt-2">
            {formData.preferred_skills.map((skill, index) => (
              <span key={index} className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800 mr-2 mb-2">
                {skill}
                <button
                  type="button"
                  onClick={() => removePreferredSkill(index)}
                  className="ml-2 flex-shrink-0 rounded-full bg-green-100 text-green-500 hover:bg-green-200 focus:outline-none"
                >
                  <span className="sr-only">Remove</span>
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div className="sm:col-span-4">
          <label htmlFor="experience_required" className="block text-sm font-medium text-gray-700">
            Experience Required
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="experience_required"
              id="experience_required"
              value={formData.experience_required}
              onChange={handleChange}
              placeholder="e.g., 3+ years"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
          </div>
        </div>

        <div className="sm:col-span-6">
          <label className="block text-sm font-medium text-gray-700">
            Role Responsibilities
          </label>
          <div className="mt-1 flex">
            <input
              type="text"
              value={newResponsibility}
              onChange={(e) => setNewResponsibility(e.target.value)}
              placeholder="Add a responsibility"
              className="flex-1 rounded-l-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            <button
              type="button"
              onClick={addResponsibility}
              className="inline-flex items-center rounded-r-md border border-l-0 border-gray-300 bg-gray-50 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Add
            </button>
          </div>
          <div className="mt-2">
            {formData.role_responsibilities.map((responsibility, index) => (
              <span key={index} className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800 mr-2 mb-2">
                {responsibility}
                <button
                  type="button"
                  onClick={() => removeResponsibility(index)}
                  className="ml-2 flex-shrink-0 rounded-full bg-blue-100 text-blue-500 hover:bg-blue-200 focus:outline-none"
                >
                  <span className="sr-only">Remove</span>
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="pt-6">
        <div className="flex justify-end">
          <button
            type="submit"
            className="ml-3 inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Create Job Posting
          </button>
        </div>
      </div>
    </form>
  );
};

export default JobDescriptionForm;
