import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { Car } from 'lucide-react';
import toast from 'react-hot-toast';

const registerSchema = z
  .object({
    name: z.string().min(1, 'Name is required').trim(),
    email: z.string().min(1, 'Email is required').email('Invalid email address').trim().toLowerCase(),
    password: z.string().min(8, 'Password must be at least 8 characters long'),
    confirm_password: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: 'Passwords do not match',
    path: ['confirm_password'],
  });

export const RegisterPage = () => {
  const { register: authRegister } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data) => {
    setLoading(true);
    try {
      await authRegister(data.name, data.email, data.password, data.confirm_password);
      toast.success('Registration successful! Please sign in.');
      navigate('/login');
    } catch (error) {
      toast.error(error.message || 'Registration failed. Try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-grid-lines relative">
      <div className="absolute inset-0 bg-radial-gradient pointer-events-none" />
      
      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <Link to="/" className="flex items-center justify-center gap-2 mb-6">
          <Car className="w-10 h-10 text-primary-500" />
          <span className="text-2xl font-black font-display tracking-wider text-white">
            ANTIGRAVITY<span className="text-primary-500">MOTORS</span>
          </span>
        </Link>
        <h2 className="text-center text-3xl font-black tracking-tight text-white uppercase font-display">
          Create <span className="text-primary-400">Account</span>
        </h2>
        <p className="mt-2 text-center text-sm text-slate-400">
          Already registered?{' '}
          <Link to="/login" className="font-semibold text-primary-400 hover:text-primary-300">
            Sign in to your account
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="glass-panel py-8 px-4 shadow sm:rounded-2xl sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            
            <Input
              label="Full Name"
              placeholder="Alice Smith"
              error={errors.name}
              {...register('name')}
            />

            <Input
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              error={errors.email}
              {...register('email')}
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              error={errors.password}
              {...register('password')}
            />

            <Input
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              error={errors.confirm_password}
              {...register('confirm_password')}
            />

            <div className="pt-2">
              <Button type="submit" loading={loading} className="w-full">
                Register Account
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
