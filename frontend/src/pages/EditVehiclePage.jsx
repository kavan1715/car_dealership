import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useNavigate, useParams } from 'react-router-dom';
import { AdminSidebar } from '../components/AdminSidebar';
import { AdminNavbar } from '../components/AdminNavbar';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { Spinner } from '../components/Spinner';
import api from '../services/api';
import toast from 'react-hot-toast';

const vehicleSchema = z.object({
  make: z.string().min(1, 'Make is required').trim(),
  model: z.string().min(1, 'Model is required').trim(),
  category: z.string().min(1, 'Category is required').trim(),
  price: z.string()
    .min(1, 'Price is required')
    .refine((val) => !isNaN(parseFloat(val)) && parseFloat(val) > 0, {
      message: 'Price must be a positive number',
    }),
  quantity: z.string()
    .min(1, 'Quantity is required')
    .refine((val) => !isNaN(parseInt(val, 10)) && parseInt(val, 10) >= 0, {
      message: 'Quantity must be zero or a positive integer',
    }),
});

export const EditVehiclePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [photoBase64, setPhotoBase64] = useState('');

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(vehicleSchema),
  });

  // Load existing data
  useEffect(() => {
    const fetchVehicle = async () => {
      try {
        const response = await api.get(`/vehicles/${id}`);
        const data = response.data;
        
        // Feed form values
        setValue('make', data.make);
        setValue('model', data.model);
        setValue('category', data.category);
        setValue('price', data.price.toString());
        setValue('quantity', data.quantity.toString());

        // Prefill photo from localStorage
        const storedPhoto = localStorage.getItem(`vehicle_image_${id}`);
        if (storedPhoto) {
          setPhotoBase64(storedPhoto);
        }
      } catch (err) {
        toast.error('Failed to load vehicle specifications.');
        navigate('/admin/vehicles');
      } finally {
        setLoading(false);
      }
    };

    fetchVehicle();
  }, [id, setValue, navigate]);

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const onSubmit = async (data) => {
    setSubmitting(true);
    try {
      const payload = {
        make: data.make,
        model: data.model,
        category: data.category,
        price: parseFloat(data.price),
        quantity: parseInt(data.quantity, 10),
      };

      await api.put(`/vehicles/${id}`, payload);

      // Save photo to localStorage
      if (photoBase64) {
        localStorage.setItem(`vehicle_image_${id}`, photoBase64);
      }

      toast.success('Specifications updated successfully!');
      navigate('/admin/vehicles');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update specs catalog entry.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex">
      <AdminSidebar />

      <div className="flex-grow flex flex-col min-w-0">
        <AdminNavbar title="Edit Specifications" />

        <main className="p-8 max-w-2xl w-full">
          {loading ? (
            <div className="h-96 flex items-center justify-center">
              <Spinner size="lg" />
            </div>
          ) : (
            <div className="glass-panel p-8 rounded-2xl">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <Input
                    label="Make / Brand"
                    error={errors.make}
                    {...register('make')}
                  />

                  <Input
                    label="Model Specification"
                    error={errors.model}
                    {...register('model')}
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Category Segment</label>
                  <select
                    className="w-full bg-[#111625]/80 text-slate-300 rounded-xl px-4 py-3 border border-slate-800 outline-none text-sm cursor-pointer"
                    {...register('category')}
                  >
                    <option value="SUV">SUV</option>
                    <option value="Sedan">Sedan</option>
                    <option value="Coupe">Coupe</option>
                    <option value="Sports">Sports</option>
                  </select>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <Input
                    label="MSRP Price (INR)"
                    type="number"
                    step="0.01"
                    error={errors.price}
                    {...register('price')}
                  />

                  <Input
                    label="Current Inventory Quantity"
                    type="number"
                    error={errors.quantity}
                    {...register('quantity')}
                  />
                </div>

                {/* Photo Upload Field */}
                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Vehicle Photo</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handlePhotoChange}
                    className="w-full bg-[#111625]/85 text-slate-350 rounded-xl px-4 py-2.5 border border-slate-800 outline-none text-sm cursor-pointer file:mr-4 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-primary-950 file:text-primary-400 hover:file:bg-primary-900 transition-colors"
                  />
                  {photoBase64 && (
                    <div className="mt-2">
                      <p className="text-[10px] text-slate-500 mb-1">Image Preview:</p>
                      <img src={photoBase64} alt="Preview" className="w-32 h-20 object-cover rounded-lg border border-slate-800" />
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-850">
                  <Button 
                    variant="secondary" 
                    onClick={() => navigate('/admin/vehicles')}
                    disabled={submitting}
                  >
                    Cancel
                  </Button>
                  <Button type="submit" loading={submitting}>
                    Update Specs
                  </Button>
                </div>
              </form>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
