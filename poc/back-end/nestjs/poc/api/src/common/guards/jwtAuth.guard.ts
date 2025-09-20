import { Injectable, UnauthorizedException, ForbiddenException, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { AuthGuard } from '@nestjs/passport';
import {IS_PUBLIC_KEY} from '../decorators/public.decorator'

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }
  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) return true;
    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any, context: any) {
    if (info?.name === 'TokenExpiredError') {
      throw new UnauthorizedException('Token expired');
    }
    
    if (info?.name === 'JsonWebTokenError') {
      throw new UnauthorizedException('Invalid Token');
    }
    
    if (info?.name === 'NotBeforeError') {
      throw new ForbiddenException('Token not yet valid');
    }
    
    if (err || !user) {
      throw err || new UnauthorizedException('Authentication required');
    }
    
    return user;
  }
}
